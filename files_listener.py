import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
import subprocess
import config

global sender_logger, error_logger, watchdog_logger


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global sender_logger, error_logger, watchdog_logger
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
    global sender_logger, error_logger, watchdog_logger
    files = os.listdir(directory)
    print(watchdog_logger())
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


def files_listener(directory, logger1, logger2, logger3):
    global sender_logger, error_logger, watchdog_logger
    sender_logger = logger1
    watchdog_logger = logger2
    error_logger = logger3
    scan_directory(directory)
    start_watchdog(directory)
