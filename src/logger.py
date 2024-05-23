import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from configs import config as config


def configure_logger(logger_name: str, log_files: dict):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    for file_name, level in log_files.items():
        handler = TimedRotatingFileHandler(
            file_name, when="midnight", interval=1, backupCount=7
        )
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

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

error_success_log_files = {
    k: v
    for k, v in log_files.items()
    if "error_watchdog" in k or "success_transfer" in k or "debug" in k
}
detected_files_log_files = {k: v for k, v in log_files.items() if "detected_files" in k}

error_or_success_logger = configure_logger("error_or_success", error_success_log_files)
detected_files_logger = configure_logger(
    "detected_files_logger", detected_files_log_files
)
