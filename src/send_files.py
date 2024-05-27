import os
import requests
from file_operations import (
    remove_extension,
    remove_files_from_os,
    list_files_by_request_format,
)
from redis_operations import RedisStorage
from configs import config as config
from logger import error_or_success_logger
from base_storage import AbstractBaseStorage

session = requests.Session()


def get_storage(storage_type: str) -> AbstractBaseStorage:
    if storage_type == "redis":
        return RedisStorage()
    else:
        error_or_success_logger.error(f"Unsupported storage type: {storage_type}")
        raise ValueError(f"Unsupported storage type: {storage_type}")


def classifyFiles(curr_filename: str):
    storage = get_storage(config.STORAGE_TYPE)
    error_or_success_logger.debug(f"opened new process for {curr_filename}")

    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]

    try:
        if storage.save(full_file_name, curr_filename):
            error_or_success_logger.debug("no key exists, key saved")
        else:
            handle_existing_key(storage, full_file_name, curr_filename)
    except Exception as e:
        error_or_success_logger.error(f"Error in classifyFiles: {e}")


def handle_existing_key(
    storage: AbstractBaseStorage, full_file_name: str, curr_filename: str
):
    error_or_success_logger.debug("key does exists")
    first_file_name = storage.get(full_file_name)

    if first_file_name != curr_filename:
        files_to_send = list_files_by_request_format(curr_filename, first_file_name)
        send_http_request(curr_filename, first_file_name, files_to_send)
        remove_files_from_os(first_file_name, curr_filename)
    else:
        error_or_success_logger.warning("Duplicate files were sent")


def send_http_request(filename: str, first_file_name: str, files_to_send: list):
    try:
        response = session.post(
            f"http://{config.HAPROXY_SERVER_IP}:{config.HAPROXY_SERVER_PORT}/merge_and_sign",
            files=files_to_send,
        )
        error_or_success_logger.debug("sending http request...")
        if response.status_code == 200:
            error_or_success_logger.info(f"File '{first_file_name}' sent successfully.")
            error_or_success_logger.info(f"File '{filename}' sent successfully.")
        else:
            error_or_success_logger.error(
                f"Error sending file '{first_file_name}': {response.status_code} {response.reason}"
            )
            error_or_success_logger.error(
                f"Error sending file '{filename}': {response.status_code} {response.reason}"
            )
    except Exception as e:
        error_or_success_logger.error(f"Exception occurred: {e}")
