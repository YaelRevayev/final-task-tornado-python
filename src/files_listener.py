import time
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from send_files import classifyFiles
import os
import sys
import subprocess
import logging
from datetime import datetime
from logger import configure_logger

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
src_dir = os.path.join(project_dir, "config")
sys.path.append(project_dir)
sys.path.insert(0, src_dir)
import configs.config as config

global sender_logger
global watchdog_logger
global error_logger

sender_logger = configure_logger(
    "sender_logger",
    os.path.join(
        config.LOGS_FOLDER_NAME,
        f"success_transfer{datetime.now().strftime('%Y-%m-%d')}.log",
    ),
    logging.INFO,
)

error_logger = configure_logger(
    "error_logger",
    os.path.join(config.LOGS_FOLDER_NAME, "error_watchdog.log"),
    logging.ERROR,
)

watchdog_logger = configure_logger(
    "watchdog_logger",
    os.path.join(
        config.LOGS_FOLDER_NAME,
        f"detected_files{datetime.now().strftime('%Y-%m-%d')}.log",
    ),
    logging.INFO,
)


class NewFileHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        global sender_logger, error_logger, watchdog_logger
        filename = event.src_path
        watchdog_logger.info(f"New file detected: {os.path.basename(filename)}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(
                filename,
                sender_logger,
                error_logger,
            ),
        ).start()


def start_watchdog(directory, run_indefinitely=True):
    patterns = ["*"]
    ignore_directories = True
    event_handler = NewFileHandler(
        patterns=patterns, ignore_directories=ignore_directories
    )
    observer = Observer()
    observer.schedule(
        event_handler,
        directory,
        recursive=True,
    )
    observer.start()
    if run_indefinitely:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
    else:
        time.sleep(0.1)
        observer.stop()
        observer.join()


def scan_directory(directory):
    global watchdog_logger, sender_logger, error_logger
    files = os.listdir(directory)
    for file in files:
        watchdog_logger.info(f"Detected file: {file}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(
                file,
                sender_logger,
                error_logger,
            ),
        ).start()


def listen_for_file_expiration():
    subprocess.run(["bash", config.SCRIPT_PATH, config.DIRECTORY_TO_WATCH])


def files_listener(directory):
    scan_directory(directory)
    start_watchdog(directory)
