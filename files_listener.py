import time
import redis
import os
import requests
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class NewFileHandler(FileSystemEventHandler):
    async def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        print(f"New file detected: {filename}")
        classifyFiles(filename)

async def classifyFiles(filename):
    file_part = remove_extension(filename)[-1]
    if  file_part == 'a':
        save_to_redis(filename)
        watch_for_second_part(filename)
    elif file_part == 'b':
        first_file = redis_client.get(filename[:-1] + 'ab')
        files = [{"file": open(first_file, "rb")},{"file": open(filename, "rb")}]
        response = requests.post("http://localhost:8000/uploadfiles/", files=files)


async def watch_for_second_part(file_a):
    await asyncio.sleep(60)
    if not os.path.exists(remove_extension(file_a) + 'b'):
        if os.path.exists(file_a):
            os.remove(file_a)
            print(f"File '{file_a}' deleted safely.")

def save_to_redis(filename):
    redis_client.rpush(remove_extension(filename) + 'b', filename)

def scan_directory(directory):
    files = os.listdir(directory)
    print("Files in directory:")
    for file in files:
        print(file)


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
