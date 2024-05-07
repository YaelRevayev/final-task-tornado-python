import logging
import os
from datetime import datetime
import configs.config as config


def configure_logger(logger_name, log_file_name):
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def create_loggers():
    sender_logger = configure_logger(
        "sender_logger",
        os.path.join(
            config.LOGS_FOLDER_NAME,
            f"success_transfer{datetime.now().strftime('%Y-%m-%d')}.log",
        ),
    )
    sender_logger.setLevel(logging.INFO)

    error_logger = configure_logger(
        "error_logger",
        os.path.join(config.LOGS_FOLDER_NAME, "error_watchdog.log"),
    )
    error_logger.setLevel(logging.ERROR)

    watchdog_logger = configure_logger(
        "watchdog_logger",
        os.path.join(
            config.LOGS_FOLDER_NAME,
            f"detected_files{datetime.now().strftime('%Y-%m-%d')}.log",
        ),
    )
    watchdog_logger.setLevel(logging.INFO)
    return (sender_logger, watchdog_logger, error_logger)
