import time
from configs import config as config
from multiprocessing import Pool
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from send_files import classifyFiles
import os
import subprocess
from datetime import datetime
from logger import detected_files_logger, error_or_success_logger


class NewFileHandler(PatternMatchingEventHandler):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    def on_modified(self, event):
        filename = event.src_path
        error_or_success_logger.debug(f"detected new file creation")
        detected_files_logger.info(f"New file detected: {os.path.basename(filename)}")
        self.pool.apply_async(classifyFiles, args=(filename,))


def scan_directory(directory: str, pool):
    files = os.listdir(directory)
    for file in files:
        detected_files_logger.info(f"Detected file: {file}")
        pool.apply_async(classifyFiles, args=(os.path.join(directory, file),))


def start_watchdog(directory: str, pool):
    observer = Observer()
    observer.schedule(NewFileHandler(pool), directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def listen_for_file_expiration():
    error_or_success_logger.debug(f"Starting script monitoring file created over 1m")
    subprocess.run(["bash", config.SCRIPT_PATH, config.DIRECTORY_TO_WATCH])


def files_listener(directory):
    pool = Pool()
    scan_directory(directory, pool)
    start_watchdog(directory, pool)
