import logging
import os
from datetime import datetime
import configs as config

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def configure_logger(logger_name, log_file_names, log_levels):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    # Clear existing handlers to avoid duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    for file_name in log_file_names:
        handler = logging.FileHandler(file_name)
        handler.setFormatter(formatter)
        handler.setLevel(log_levels[file_name])
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)
    return logger


first_log_file_names = [
    os.path.join(project_dir, config.LOGS_FOLDER_NAME, "error_watchdog.log"),
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"success_transfer{datetime.now().strftime('%Y-%m-%d')}.log",
    ),
]

second_log_file_name = [
    os.path.join(
        project_dir,
        config.LOGS_FOLDER_NAME,
        f"detected_files{datetime.now().strftime('%Y-%m-%d')}.log",
    )
]

log_levels = {
    first_log_file_names[0]: logging.ERROR,
    first_log_file_names[1]: logging.INFO,
    second_log_file_name[0]: logging.INFO,
}

error_success_logger = configure_logger(
    "error_success_logger", first_log_file_names, log_levels
)
detected_files_logger = configure_logger(
    "detected_files_logger", second_log_file_name, log_levels
)
