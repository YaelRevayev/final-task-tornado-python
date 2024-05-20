import time
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from send_files import (
    classifyFiles,
)
import os
import subprocess
from datetime import datetime
import configs as config


class NewFileHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        from logger import detected_files_logger

        filename = event.src_path
        detected_files_logger.info(f"New file detected: {os.path.basename(filename)}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(filename,),
        ).start()


def start_watchdog(directory):
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def scan_directory(directory):
    from logger import detected_files_logger

    files = os.listdir(directory)
    for file in files:
        if file == ".gitkeep":
            continue
        detected_files_logger.info(f"Detected file: {file}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(os.path.join(directory, file),),
        ).start()


def listen_for_file_expiration():
    subprocess.run(["bash", config.SCRIPT_PATH, config.DIRECTORY_TO_WATCH])


def files_listener(directory):
    scan_directory(directory)
    start_watchdog(directory)
