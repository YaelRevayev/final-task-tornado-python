import logging
import logging.handlers
import os
from datetime import datetime
from multiprocessing import Queue, Process, Lock
from configs import config

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def configure_logger(queue, logger_name: str, log_files: dict):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # QueueHandler sends logs to the queue
    handler = logging.handlers.QueueHandler(queue)
    logger.addHandler(handler)

    return logger


def listener_configurer(log_files: dict):
    root = logging.getLogger()
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )

    for file_name, level in log_files.items():
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root.addHandler(file_handler)


def log_listener(queue, log_files):
    listener_configurer(log_files)
    listener = logging.handlers.QueueListener(queue, *logging.getLogger().handlers)
    listener.start()
    listener.join()


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

log_queue = Queue()

error_or_success_logger = configure_logger(
    log_queue, "error_success_logger", error_success_log_files
)
detected_files_logger = configure_logger(
    log_queue, "detected_files_logger", detected_files_log_files
)

listener_process = Process(target=log_listener, args=(log_queue, log_files))
listener_process.start()
