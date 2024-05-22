import logging
import os
from datetime import datetime
from configs import config as config


def configure_logger(logger_name: str, log_files: dict):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Set the logger level to DEBUG to log all messages

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    for file_name, level in log_files.items():
        handler = logging.FileHandler(file_name)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    return logger


project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

log_files = {
    os.path.join(
        project_dir, config.LOGS_FOLDER_NAME, "error_watchdog.log"
    ): logging.ERROR,
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"success_transfer_{datetime.now().strftime('%Y-%m-%d')}.log",
    ): logging.INFO,
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"detected_files_{datetime.now().strftime('%Y-%m-%d')}.log",
    ): logging.INFO,
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"debug_{datetime.now().strftime('%Y-%m-%d')}.log",
    ): logging.DEBUG,
}

error_or_success_logger = configure_logger("error_success_logger", log_files)
detected_files_logger = configure_logger("detected_files_logger", log_files)
