import logging
import os
from datetime import datetime
from configs import config

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def configure_logger(logger_name: str, log_files: dict):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    for file_name, level in log_files.items():
        handler = logging.FileHandler(file_name)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)
    return logger


log_files = {
    os.path.join(
        project_dir, config.LOGS_FOLDER_NAME, "error_watchdog.log"
    ): logging.ERROR,
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"success_transfer{datetime.now().strftime('%Y-%m-%d')}.log",
    ): logging.INFO,
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"detected_files{datetime.now().strftime('%Y-%m-%d')}.log",
    ): logging.INFO,
}

# Split the log files for different loggers
error_success_log_files = {
    k: v
    for k, v in log_files.items()
    if "error_watchdog" in k or "success_transfer" in k
}
detected_files_log_files = {k: v for k, v in log_files.items() if "detected_files" in k}

error_or_success_logger = configure_logger(
    "error_success_logger", error_success_log_files
)
detected_files_logger = configure_logger(
    "detected_files_logger", detected_files_log_files
)
