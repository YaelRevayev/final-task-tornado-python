import time
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from send_files import classifyFiles
import os
import subprocess
from datetime import datetime
from logger import detected_files_logger
import configs as config


class NewFileHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        filename = event.src_path
        detected_files_logger.info(f"New file detected: {os.path.basename(filename)}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(filename),
        ).start()


def start_watchdog(directory, run_indefinitely=True):
    patterns = ["*"]
    ignore_directories = True
    event_handler = NewFileHandler(
        patterns=patterns,
        ignore_directories=ignore_directories,
    )
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        if run_indefinitely:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()


def scan_directory(directory):
    files = os.listdir(directory)
    for file in files:
        detected_files_logger.info(f"Detected file: {file}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(file),
        ).start()


def listen_for_file_expiration():
    subprocess.run(["bash", config.SCRIPT_PATH, config.DIRECTORY_TO_WATCH])


def files_listener(directory):
    scan_directory(directory)
    start_watchdog(directory)
