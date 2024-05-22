import os
import requests
from file_operations import (
    remove_extension,
    remove_file_from_os,
    list_files,
)
from redis_operations import RedisStorage
from configs import config as config
from logger import error_or_success_logger
from base_storage import BaseStorage
import multiprocessing

lock = multiprocessing.Lock()


def get_storage(storage_type: str) -> BaseStorage:
    if storage_type == "redis":
        return RedisStorage()
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")


def classifyFiles(curr_filename: str):
    storage = get_storage(config.STORAGE_TYPE)
    error_or_success_logger.debug(f"opened new process for {curr_filename}")
    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]

    try:
        # Acquire lock to ensure exclusive access
        lock.acquire()
        error_or_success_logger.debug("classify files ---> ....")
        if not storage.exists(full_file_name):
            storage.save(full_file_name, curr_filename)
        else:
            first_file_name = storage.get(full_file_name)
            if first_file_name != curr_filename:
                files_to_send = list_files(curr_filename, first_file_name)
                send_http_request(curr_filename, first_file_name, files_to_send)
                remove_file_from_os(config.DIRECTORY_TO_WATCH, first_file_name)
                remove_file_from_os(config.DIRECTORY_TO_WATCH, curr_filename)
        lock.release()
    except Exception as e:
        error_or_success_logger.error(f"Error in classifyFiles: {e}")


def process_file():
    pass


def send_http_request(filename: str, first_file_name: str, files_to_send: list):
    try:
        response = requests.post(
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
