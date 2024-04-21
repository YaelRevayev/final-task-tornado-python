import os
import requests
import redis
import config
from file_operations import read_file, remove_extension

redis_client = redis.StrictRedis(
    host=config.REDIS_HOST_IP, port=config.REDIS_HOST_PORT, db=0
)


def classifyFiles(curr_filename, sender_logger, error_logger):

    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]
    key_exists = redis_client.exists(full_file_name)

    if not key_exists:
        save_to_redis(full_file_name, curr_filename)

    elif key_exists:
        first_file_name = redis_client.get(full_file_name).decode("utf-8")
        if first_file_name != curr_filename:
            files_to_send = list_files_in_order(curr_filename, first_file_name)
            send_http_request(
                curr_filename,
                first_file_name,
                files_to_send,
                sender_logger,
                error_logger,
            )
            os.remove(("{0}/{1}").format(config.DIRECTORY_TO_WATCH, first_file_name))
            os.remove(("{0}/{1}").format(config.DIRECTORY_TO_WATCH, curr_filename))


def part_a_or_b(filename):
    index_of_underscore = filename.find("_")
    if index_of_underscore != -1 and index_of_underscore + 1 < len(filename):
        return filename[index_of_underscore + 1]
    else:
        return None


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
    print(files_to_send)
    return files_to_send


def send_http_request(
    filename, first_file_name, files_to_send, sender_logger, error_logger
):
    response = requests.post(
        "http://{ip}:{port}/merge_and_sign".format(
            ip=config.HAPROXY_SERVER_IP, port=config.HAPROXY_SERVER_PORT
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


def save_to_redis(key, value):
    redis_client.set(key, value, ex=config.EXPIRY_SECONDS)
    redis_client.expire(key, config.EXPIRY_SECONDS)
