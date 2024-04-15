import time
import threading
from logger import configure_logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
from datetime import datetime


global info_logger
global error_logger


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        info_logger.info(f"New file detected: {filename}")
        threading.Thread(
            target=classifyFiles,
            args=(
                filename,
                info_logger,
                error_logger,
            ),
        ).start()


def start_watchdog(directory):
    observer = Observer()
    observer.schedule(NewFileHandler(), directory, recursive=True)
    observer.start()
    info_logger.info(f"Watching directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def scan_directory(directory):
    files = os.listdir(directory)
    info_logger.info("Scanned files in directory:")
    for file in files:
        info_logger.info(file)
        threading.Thread(
            target=classifyFiles,
            args=(
                file,
                info_logger,
                error_logger,
            ),
        ).start()


def files_listener(directory):
    global info_logger, error_logger
    error_logger = configure_logger(
        "error_logger",
        os.path.join("logs", "error_watchdog.log"),
    )
    info_logger = configure_logger(
        "info_logger",
        os.path.join(
            "logs", f"success_watchdog{datetime.now().strftime('%Y-%m-%d')}.log"
        ),
    )

    scan_directory(directory)
    start_watchdog(directory)
