import os
import time
import requests
import threading
import redis
from logger import logger,error_logger


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def classifyFiles(filename):
    file_part = remove_extension(filename)[-1]
    if  file_part == 'a':
        save_to_redis(filename)
        threading.Thread(target=watch_for_second_part,args=(filename,)).start()

    elif file_part == 'b':
        first_file = redis_client.get(filename[:-1] + 'ab')
        files = [{"file": open(first_file, "rb")},{"file": open(filename, "rb")}]
        #response = requests.post("http://localhost:8000/uploadfiles/", files=files)
        #if response.status_code == 200:
            #logger.info(f"File '{filename}' sent successfully.")
        #else:
            #error_logger.error(f"Error sending file '{filename}': {response.status_code} {response.reason}")

def watch_for_second_part(file_a):
    time.sleep(60)
    if not os.path.exists(remove_extension(file_a)[:-1] + 'b'):
        if os.path.exists(file_a):
            os.remove(file_a)
            logger.info(f"File '{file_a}' deleted - couldn't find second part of the file.")

def save_to_redis(filename):
    redis_client.rpush(remove_extension(filename) + 'b', filename)

def remove_extension(filename):
    base_filename, _ = os.path.splitext(filename)
    return base_filename