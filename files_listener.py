import time
import threading
from logger import LoggerSingleton
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
import subprocess
import config

global info_logger
global error_logger
global sender_logger


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global watchdog_logger
        if event.is_directory:
            return
        filename = event.src_path
        watchdog_logger.info(f"New file detected: {filename}")
        threading.Thread(
            target=classifyFiles,
            args=(filename,),
        ).start()


def start_watchdog(directory):
    global watchdog_logger
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
    global watchdog_logger
    files = os.listdir(directory)
    watchdog_logger.info("Scanned files in directory:")
    for file in files:
        watchdog_logger.info(file)
        threading.Thread(
            target=classifyFiles,
            args=(file,),
        ).start()


def listen_for_file_expiration():
    subprocess.run(["bash", config.SCRIPT_PATH])


def files_listener(directory):
    global watchdog_logger, error_logger, sender_logger
    logger_instance = LoggerSingleton()

    sender_logger = logger_instance.sender_logger
    error_logger = logger_instance.error_logger
    watchdog_logger = logger_instance.watchdog_logger
    print(watchdog_logger)

    scan_directory(directory)
    start_watchdog(directory)
