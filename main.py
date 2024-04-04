from files_listener import start_watchdog
import os
from logger import configure_error_logger,configure_success_logger,reset_folder


def scan_directory(directory):
    info_logger = configure_success_logger()
    files = os.listdir(directory)
    info_logger.info("Scanned files in directory:")                                                     
    for file in files:
        info_logger.info(file)

if __name__ == "__main__":
    reset_folder("logs")
    reset_folder("files_output")
    directory_to_watch = "/home/pure-ftpd-server/final-task-tornado-python"
    scan_directory(directory_to_watch)
    start_watchdog(directory_to_watch)

