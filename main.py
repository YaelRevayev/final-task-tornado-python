import time
import redis
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Connect to Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        print(f"New file detected: {filename}")
        save_to_redis(filename)



def classifyFiles(filename):
    file_part = remove_extension(filename)[-1]
    if  file_part == 'a':
        save_to_redis(filename)
    elif file_part == 'b':
        redis_client.get(filename[:-1] + 'ab')



def save_to_redis(filename):
    redis_client.rpush(remove_extension(filename) + 'b', filename)


def start_watchdog(directory):
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()
    print(f"Watching directory: {directory}")

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
    directory_to_watch = "/home/pure-ftpd-server/files_output"
    start_watchdog(directory_to_watch)
