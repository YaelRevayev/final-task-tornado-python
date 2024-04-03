import os
import time
import requests
import threading
import redis
from logger import logger,error_logger
import constant


redis_client = redis.StrictRedis(host=constant.REDIS_HOST_IP, port=constant.REDIS_HOST_PORT, db=0)

def classifyFiles(filename):
    file_part = remove_extension(filename)[-1]
    if  file_part == 'a':
        save_to_redis(filename)
        threading.Thread(target=watch_for_second_part,args=(filename,)).start()

    elif file_part == 'b':
        first_file_name = redis_client.get(filename[:-1] + 'ab').decode('utf-8')
        files_to_send = []
        files_to_send.append(("files", (os.path.basename(first_file_name), read_file(first_file_name))))
        files_to_send.append(("files", (os.path.basename(filename), read_file(filename))))
        response = requests.post("http://{ip}:{port}/merge_and_sign".format(ip = constant.HAPROXY_SERVER_IP,
                                                                      port = constant.HAPROXY_SERVER_PORT),
                                                                        files=files_to_send)
        if response.status_code == 200:
            logger.info(f"Files '{first_file_name}' , '{filename}' sent successfully.")
        else:
            error_logger.error(f"Error sending files '{first_file_name}' , '{filename}': {response.status_code} {response.reason}")

def watch_for_second_part(file_a):
    time.sleep(60)
    if not os.path.exists(remove_extension(file_a)[:-1] + 'b'):
        if os.path.exists(file_a):
            os.remove(file_a)
            logger.info(f"File '{file_a}' deleted - couldn't find second part of the file.")

def save_to_redis(filename):
    redis_client.set(remove_extension(filename) + 'b', filename)

def read_file(filename):
    with open(filename, "rb") as file:
            file_data = file.read()

    return file_data

def remove_extension(filename):
    base_filename, _ = os.path.splitext(filename)
    return base_filename
