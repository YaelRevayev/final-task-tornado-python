import time
import threading
<<<<<<< HEAD
=======
from logger import configure_error_logger,configure_success_logger
>>>>>>> ef0307fac2214789132c071fd4a2f206f3cb0bbd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_files import classifyFiles
import os
<<<<<<< HEAD
import subprocess
from logger import create_loggers
import config

=======

global info_logger
global error_logger
>>>>>>> ef0307fac2214789132c071fd4a2f206f3cb0bbd

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, sender_logger, error_logger, watchdog_logger):
        self.sender_logger = sender_logger
        self.error_logger = error_logger
        self.watchdog_logger = watchdog_logger

    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
<<<<<<< HEAD
        self.watchdog_logger.info(f"New file detected: {os.path.basename(filename)}")
        threading.Thread(
            target=classifyFiles,
            args=(
                filename,
                self.sender_logger,
                self.error_logger,
            ),
        ).start()
=======
        info_logger.info(f"New file detected: {filename}")
        threading.Thread(target=classifyFiles,args=(filename,info_logger,error_logger,)).start()
>>>>>>> ef0307fac2214789132c071fd4a2f206f3cb0bbd


def start_watchdog(
    directory, sender_logger, error_logger, watchdog_logger, run_indefinitely=True
):
    observer = Observer()
    observer.schedule(
        NewFileHandler(sender_logger, error_logger, watchdog_logger),
        directory,
        recursive=True,
    )
    observer.start()
    watchdog_logger.info(f"Watching directory: {directory}")
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

def scan_directory(directory, sender_logger, error_logger, watchdog_logger):
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
    sender_logger, watchdog_logger, error_logger = create_loggers()
    scan_directory(directory, sender_logger, error_logger, watchdog_logger)
    start_watchdog(directory, sender_logger, error_logger, watchdog_logger)
