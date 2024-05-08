import logging
from datetime import datetime


def configure_logger(logger_name, log_file_name, log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger
