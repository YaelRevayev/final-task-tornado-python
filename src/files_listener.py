import time
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.send_files import classifyFiles
import os
import subprocess
from src.logger import create_loggers
import config.config as config

sender_logger = None
watchdog_logger = None
error_logger = None


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
    global sender_logger, error_logger, watchdog_logger
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
    global sender_logger, error_logger, watchdog_logger
    files = os.listdir(directory)
    for file in files:
        watchdog_logger.info(file)
        multiprocessing.Process(
            target=classifyFiles,
            args=(
                file,
                sender_logger,
                error_logger,
            ),
        ).start()


def listen_for_file_expiration():
    global config
    subprocess.run(["bash", config.SCRIPT_PATH])


def files_listener(directory):
    global sender_logger, error_logger, watchdog_logger
    sender_logger, watchdog_logger, error_logger = create_loggers()
    scan_directory(directory)
    start_watchdog(directory)
