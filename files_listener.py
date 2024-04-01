import time
import redis
import os
import requests
import threading
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('python_info.log'),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a separate logger for errors
error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(logging.FileHandler('python_error.log'))

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        logger.info(f"New file detected: {filename}")
        threading.Thread(target=classifyFiles,args=(filename,)).start()




def classifyFiles(filename):
    file_part = remove_extension(filename)[-1]
    if  file_part == 'a':
        #save_to_redis(filename)
        threading.Thread(target=watch_for_second_part,args=(filename,)).start()


    elif file_part == 'b':
        pass
        #first_file = redis_client.get(filename[:-1] + 'ab')
        #files = [{"file": open(first_file, "rb")},{"file": open(filename, "rb")}]
        #response = requests.post("http://localhost:8000/uploadfiles/", files=files)
        #if response.status_code == 200:
            #logger.info(f"File '{filename}' sent successfully.")
        #else:
            #error_logger.error(f"Error sending file '{filename}': {response.status_code} {response.reason}")

def watch_for_second_part(file_a):
    time.sleep(60)
    print(remove_extension(file_a)[:-1] + 'b')
    if not os.path.exists(remove_extension(file_a)[:-1] + 'b'):
        if os.path.exists(file_a):
            os.remove(file_a)
            logger.info(f"File '{file_a}' deleted - couldn't find second part of the file.")

def save_to_redis(filename):
    redis_client.rpush(remove_extension(filename) + 'b', filename)

def scan_directory(directory):
    files = os.listdir(directory)
    logger.info("Scanned files in directory:")
    for file in files:
        logger.info(file)

def start_watchdog(directory):
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()
    logger.info(f"Watching directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def remove_extension(filename):
    base_filename, _ = os.path.splitext(filename)
    return base_filename

if __name__ == "__main__":
    #directory_to_watch = "/home/pure-ftpd-server/files_output"
    directory_to_watch = "./testfolder"
    scan_directory(directory_to_watch)
    start_watchdog(directory_to_watch)
