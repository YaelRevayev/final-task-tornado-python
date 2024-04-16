import logging


def configure_logger(logger_name, log_file_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
