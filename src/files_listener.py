import time
from configs import config as config
from multiprocessing import Pool
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
import subprocess
from logger import (
    detected_files_logger,
    application_info_logger,
)


class NewFileHandler(FileSystemEventHandler):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    def on_closed(self, event):
        if not event.is_directory:
            filename = event.src_path
            application_info_logger.debug(f"detected new file creation")
            detected_files_logger.info(
                f"New file detected: {os.path.basename(filename)}"
            )
            self.pool.apply_async(classifyFiles, args=(filename,))


def scan_directory(directory: str, pool: multiprocessing.Pool):
    files = os.listdir(directory)
    for file in files:
        detected_files_logger.info(f"Detected file: {file}")
        pool.apply_async(classifyFiles, args=(os.path.join(directory, file),))


def start_watchdog(directory: str, pool: multiprocessing.Pool):
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
    application_info_logger.debug(f"Starting script monitoring file created over 1m")
    subprocess.run(
        ["bash", config.FILE_EXPIRATION_SCRIPT_PATH, config.DIRECTORY_TO_WATCH]
    )


def files_listener(directory):
    pool = Pool()
    scan_directory(directory, pool)
    start_watchdog(directory, pool)
