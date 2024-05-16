import os
import requests
from file_operations import (
    read_file,
    remove_extension,
    remove_file_from_os,
    list_files,
)
from redis_operations import *
import configs as config
from logger import error_success_logger


def classifyFiles(curr_filename):
    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]

    if not does_key_exists(full_file_name):
        save_to_redis(full_file_name, curr_filename)

    else:
        first_file_name = get_value_by_key(full_file_name)
        if first_file_name != curr_filename:
            files_to_send = list_files(curr_filename, first_file_name)
            send_http_request(curr_filename, first_file_name, files_to_send)
            remove_file_from_os(config.DIRECTORY_TO_WATCH, first_file_name)
            remove_file_from_os(config.DIRECTORY_TO_WATCH, curr_filename)


def send_http_request(filename, first_file_name, files_to_send):
    global sender_logger, error_logger
    try:
        response = requests.post(
            "http://{ip}:{port}/merge_and_sign".format(
                ip=config.HAPROXY_SERVER_IP,
                port=config.HAPROXY_SERVER_PORT,
            ),
            files=files_to_send,
        )
        if response.status_code == 200:
            error_success_logger.info(f"File '{first_file_name}'  sent successfully.")
            error_success_logger.info(f"File  '{filename}' sent successfully.")
        else:
            error_success_logger.error(
                f"Error sending file '{first_file_name}': {response.status_code} {response.reason}"
            )
            error_success_logger.error(
                f"Error sending file '{filename}': {response.status_code} {response.reason}"
            )
    except Exception as e:
        error_success_logger.error(f"Exception occurred: {e}")
