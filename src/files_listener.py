import time
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from send_files import (
    classifyFiles,
)  # Ensure classifyFiles takes a single filename argument
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
            args=(filename,),  # Ensure this is a tuple
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
    from logger import detected_files_logger

    files = os.listdir(directory)
    for file in files:
        detected_files_logger.info(f"Detected file: {file}")
        multiprocessing.Process(
            target=classifyFiles,
            args=(os.path.join(directory, file),),  # Ensure this is a tuple
        ).start()


def listen_for_file_expiration():
    subprocess.run(["bash", config.SCRIPT_PATH, config.DIRECTORY_TO_WATCH])


def files_listener(directory):
    scan_directory(directory)
    start_watchdog(directory)


if __name__ == "__main__":
    directory_to_watch = (
        config.DIRECTORY_TO_WATCH
    )  # Example, replace with actual directory
    files_listener(directory_to_watch)
