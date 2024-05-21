import os
import requests
from file_operations import (
    remove_extension,
    remove_file_from_os,
    list_files,
)
from redis_operations import RedisStorage
from configs import config
from logger import error_or_success_logger
from base_storage import BaseStorage
import multiprocessing


def get_storage(storage_type: str) -> BaseStorage:
    if storage_type == "redis":
        return RedisStorage()
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")


storage_type = config.STORAGE_TYPE
storage = get_storage(storage_type)
lock = multiprocessing.Lock()


def classifyFiles(curr_filename: str):
    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]

    with lock:  # Acquire lock to ensure exclusive access
        if not storage.does_key_exists(full_file_name):
            storage.save_to_redis(full_file_name, curr_filename)
        else:
            first_file_name = storage.get_value_by_key(full_file_name)
            if first_file_name != curr_filename:
                files_to_send = list_files(curr_filename, first_file_name)
                send_http_request(curr_filename, first_file_name, files_to_send)
                remove_file_from_os(config.DIRECTORY_TO_WATCH, first_file_name)
                remove_file_from_os(config.DIRECTORY_TO_WATCH, curr_filename)


def process_file():
    pass


def send_http_request(filename: str, first_file_name: str, files_to_send: list):

    try:
        response = requests.post(
            "http://{ip}:{port}/merge_and_sign".format(
                ip=config.HAPROXY_SERVER_IP,
                port=config.HAPROXY_SERVER_PORT,
            ),
            files=files_to_send,
        )
        if response.status_code == 200:
            error_or_success_logger.info(
                f"File '{first_file_name}'  sent successfully."
            )
            error_or_success_logger.info(f"File  '{filename}' sent successfully.")
        else:
            error_or_success_logger.error(
                f"Error sending file '{first_file_name}': {response.status_code} {response.reason}"
            )
            error_or_success_logger.error(
                f"Error sending file '{filename}': {response.status_code} {response.reason}"
            )
    except Exception as e:
        error_or_success_logger.error(f"Exception occurred: {e}")
