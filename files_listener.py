import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
import subprocess
from logger import create_loggers
import config

global sender_logger
global error_logger
global watchdog_logger


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        watchdog_logger.info(f"New file detected: {filename}")
        threading.Thread(
            target=classifyFiles,
            args=(
                filename,
                sender_logger,
                error_logger,
            ),
        ).start()


def start_watchdog(directory):
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()
    watchdog_logger.info(f"Watching directory: {directory}")
    print("Watching")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def scan_directory(directory):
    files = os.listdir(directory)
    print(watchdog_logger)
    watchdog_logger.info("Scanned files in directory:")
    for file in files:
        watchdog_logger.info(file)
        threading.Thread(
            target=classifyFiles,
            args=(
                file,
                sender_logger,
                error_logger,
            ),
        ).start()


def listen_for_file_expiration():
    subprocess.run(["bash", config.SCRIPT_PATH])


def files_listener(directory):
    global sender_logger, error_logger, watchdog_logger
    sender_logger, watchdog_logger, error_logger = create_loggers()
    scan_directory(directory)
    start_watchdog(directory)
