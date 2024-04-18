import time
import threading
from logger import configure_logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
import subprocess
from datetime import datetime
import config

global info_logger
global error_logger
global sender_logger


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

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def scan_directory(directory):
    files = os.listdir(directory)
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
    global watchdog_logger, error_logger, sender_logger
    error_logger = configure_logger(
        "error_logger",
        os.path.join("logs", "error_watchdog.log"),
    )
    watchdog_logger = configure_logger(
        "info_logger",
        os.path.join(
            "logs", f"detected_files{datetime.now().strftime('%Y-%m-%d')}.log"
        ),
    )
    sender_logger = configure_logger(
        "info_logger",
        os.path.join(
            "logs", f"success_transfer{datetime.now().strftime('%Y-%m-%d')}.log"
        ),
    )

    scan_directory(directory)
    start_watchdog(directory)
