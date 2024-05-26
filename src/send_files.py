import os
import requests
from file_operations import (
    remove_extension,
    remove_files_from_os,
    list_files,
)
from redis_operations import RedisStorage
from configs import config as config
from logger import error_or_success_logger
from base_storage import BaseStorage
import multiprocessing
import time

lock = multiprocessing.Lock()
session = requests.Session()


def get_storage(storage_type: str) -> BaseStorage:
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

    wait_until_file_written(f"../files_output/{curr_filename}")
    try:
        with lock:
            if not storage.exists(full_file_name):
                storage.save(full_file_name, curr_filename)
                error_or_success_logger.debug("no key exists")
            else:
                handle_existing_key(storage, full_file_name, curr_filename)
    except Exception as e:
        error_or_success_logger.error(f"Error in classifyFiles: {e}")


def wait_until_file_written(filename: str, max_wait_time=100):
    initial_size = os.path.getsize(filename)
    time_waited = 0
    while True:
        time.sleep(1)
        current_size = os.path.getsize(filename)
        if current_size == initial_size:
            time_waited += 1
            if time_waited >= max_wait_time:
                break
        else:
            initial_size = current_size
            time_waited = 0


def handle_existing_key(storage, full_file_name, curr_filename):
    error_or_success_logger.debug("key does exists")
    first_file_name = storage.get(full_file_name)

    if first_file_name != curr_filename:
        files_to_send = list_files(curr_filename, first_file_name)
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
