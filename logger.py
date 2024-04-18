import logging
import os
from datetime import datetime
import config


class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._error_logger = cls._configure_logger(
                "error_logger",
                os.path.join(config.LOGS_FOLDER_NAME, "error_watchdog.log"),
            )
            cls._instance.error_logger.setLevel(logging.ERROR)
            cls._instance._watchdog_logger = cls._configure_logger(
                "info_logger",
                os.path.join(
                    config.LOGS_FOLDER_NAME,
                    f"detected_files{datetime.now().strftime('%Y-%m-%d')}.log",
                ),
            )
            cls._instance.watchdog_logger.setLevel(logging.INFO)
            cls._instance._sender_logger = cls._configure_logger(
                "info_logger",
                os.path.join(
                    config.LOGS_FOLDER_NAME,
                    f"success_transfer{datetime.now().strftime('%Y-%m-%d')}.log",
                ),
            )
            cls._instance._sender_logger.setLevel(logging.INFO)
        return cls._instance

    @staticmethod
    def _configure_logger(logger_name, log_file_name):
        logger = logging.getLogger(logger_name)
        handler = logging.FileHandler(log_file_name)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @property
    def error_logger(self):
        return self._error_logger

    @property
    def watchdog_logger(self):
        return self._watchdog_logger

    @property
    def sender_logger(self):
        return self._sender_logger
