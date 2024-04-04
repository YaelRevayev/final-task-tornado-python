import time
import threading
from logger import configure_error_logger,configure_success_logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os

global info_logger
global error_logger

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global info_logger
        if event.is_directory:
            return
        filename = event.src_path
        info_logger.info(f"New file detected: {filename}")
        threading.Thread(target=classifyFiles,args=(filename,info_logger,error_logger,)).start()

def start_watchdog(directory):
    global info_logger
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()
    info_logger.info(f"Watching directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def scan_directory(directory):
    global info_logger
    files = os.listdir(directory)
    info_logger.info("Scanned files in directory:")                                                     
    for file in files:
        info_logger.info(file)

def main(directory):
    global info_logger
    info_logger = configure_success_logger()
    global error_logger
    error_logger = configure_error_logger()
    scan_directory(directory)
    start_watchdog(directory)
