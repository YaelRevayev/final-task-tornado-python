import logging
import os
from datetime import datetime
import shutil

#reset_folder("logs")
#reset_folder("files_output")
def reset_folder(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)

def configure_error_logger():
    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(os.path.join("logs", "error_watchdog.log"))
    error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    return error_logger


def configure_success_logger():
    info_logger = logging.getLogger("info_logger")
    info_logger.setLevel(logging.INFO)
    info_handler = logging.FileHandler(
        os.path.join("logs", f"success_watchdog{datetime.now().strftime('%Y-%m-%d')}.log")
    )       
    info_formatter = logging.Formatter(
     "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    info_handler.setFormatter(info_formatter)
    info_logger.addHandler(info_handler)
    return info_logger
