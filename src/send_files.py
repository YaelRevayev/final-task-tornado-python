import os
import requests
import sys
from file_operations import read_file, remove_extension
from redis_operations import *

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
config_dir = os.path.join(project_dir, "config")


sys.path.append(project_dir)
sys.path.insert(0, config_dir)
import configs.config as config

global sender_logger
global error_logger


def classifyFiles(curr_filename, sender_logger_instance, error_logger_instance):
    global sender_logger, error_logger
    sender_logger = sender_logger_instance
    error_logger = error_logger_instance
    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]

    if not does_key_exists(full_file_name):
        save_to_redis(full_file_name, curr_filename)

    else:
        first_file_name = get_value_by_key(full_file_name)
        if first_file_name != curr_filename:
            files_to_send = list_files_in_order(curr_filename, first_file_name)
            send_http_request(curr_filename, first_file_name, files_to_send)
            remove_file_from_os(config.DIRECTORY_TO_WATCH, first_file_name)
            remove_file_from_os(config.DIRECTORY_TO_WATCH, curr_filename)


def part_a_or_b(filename):
    index_of_underscore = filename.find("_")
    if index_of_underscore != -1 and index_of_underscore + 1 < len(filename):
        return filename[index_of_underscore + 1]
    else:
        return None


def remove_file_from_os(folder_name, file_name):
    os.remove(("{0}/{1}").format(folder_name, file_name))


def list_files_in_order(curr_file, first_file):
    files_to_send = []
    file_paths = [f"files_output/{first_file}", f"files_output/{curr_file}"]

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_content = read_file(file_path)
        part = part_a_or_b(file_name)
        if part == "a":
            files_to_send.append(("files", (file_name, file_content)))

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_content = read_file(file_path)
        part = part_a_or_b(file_name)
        if part == "b":
            files_to_send.append(("files", (file_name, file_content)))
    return files_to_send


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
            sender_logger.info(
                f"Files '{first_file_name}' , '{filename}' sent successfully."
            )
        else:
            error_logger.error(
                f"Error sending files '{first_file_name}' , '{filename}': {response.status_code} {response.reason}"
            )
    except Exception as e:
        error_logger.error(f"Exception occurred: {e}")
