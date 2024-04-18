import os
import requests
import redis
import config
from file_operations import read_file, remove_extension
from logger import LoggerSingleton

redis_client = redis.StrictRedis(
    host=config.REDIS_HOST_IP, port=config.REDIS_HOST_PORT, db=0
)


def classifyFiles(curr_filename, first_logger, second_logger):

    curr_filename = os.path.basename(curr_filename)
    full_file_name = remove_extension(curr_filename)[:-2]
    key_exists = redis_client.exists(full_file_name)

    if not key_exists:
        save_to_redis(full_file_name, curr_filename)

    elif key_exists:
        first_file_name = redis_client.get(full_file_name).decode("utf-8")
        files_to_send = list_files_in_order(curr_filename, first_file_name)
        send_http_request(curr_filename, first_file_name, files_to_send)
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
    # send file a as the first file and file b as the second file
    file_identifier = part_a_or_b(curr_file)
    if file_identifier == "b":
        files_to_send.append(
            ("files", first_file, read_file("./files_output/" + first_file))
        )
        files_to_send.append(
            ("files", curr_file, read_file("./files_output/" + curr_file))
        )
    elif file_identifier == "a":
        files_to_send.append(
            ("files", curr_file, read_file("./files_output/" + curr_file))
        )
        files_to_send.append(
            ("files", first_file, read_file("./files_output/" + first_file))
        )
    return files_to_send


def send_http_request(first_file_name, filename, files_to_send):
    logger_instance = LoggerSingleton()
    sender_logger = logger_instance.sender_logger
    error_logger = logger_instance.error_logger
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
    # Set expiration time for the key 'mykey' to 60 seconds
    redis_client.expire(key, 60)
