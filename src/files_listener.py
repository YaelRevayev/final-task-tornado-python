import time
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
import sys
import subprocess
from logger import create_loggers

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
src_dir = os.path.join(project_dir, "config")
sys.path.append(project_dir)
sys.path.insert(0, src_dir)
import configs.config

global sender_logger
global watchdog_logger
global error_logger


class NewFileHandler(FileSystemEventHandler):

    def on_created(self, event):
        global sender_logger, error_logger, watchdog_logger
        if event.is_directory:
            return
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
    observer = Observer()
    observer.schedule(
        NewFileHandler(),
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
        time.sleep(0.1)  # Short delay to allow the observer to start
        observer.stop()
        observer.join()


def scan_directory(directory):
    global watchdog_logger
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
    subprocess.run(
        ["bash", configs.config.SCRIPT_PATH, configs.config.DIRECTORY_TO_WATCH]
    )


def files_listener(directory):
    global sender_logger, error_logger, watchdog_logger
    sender_logger, watchdog_logger, error_logger = create_loggers()
    scan_directory(directory)
    start_watchdog(directory)
