from files_listener import start_watchdog
import os
from logger import logger

def scan_directory(directory):
    files = os.listdir(directory)
    logger.info("Scanned files in directory:")
    for file in files:
        logger.info(file)

def main():
    directory_to_watch = "/home/pure-ftpd-server/files_output"
    scan_directory(directory_to_watch)
    start_watchdog(directory_to_watch)

if __name__ == "__main__":
    main()

