from files_listener import files_listener, listen_for_file_expiration
import config
from logger import create_loggers


def main():
    sender_logger, watchdog_logger, error_logger = create_loggers()
    print(watchdog_logger)
    listen_for_file_expiration()
    files_listener(
        config.DIRECTORY_TO_WATCH, sender_logger, watchdog_logger, error_logger
    )


if __name__ == "__main__":
    main()
