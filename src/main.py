from configs import config as config
from files_listener import files_listener, listen_for_file_expiration
import multiprocessing
from logger import error_or_success_logger


def main():
    try:
        multiprocessing.Process(
            target=listen_for_file_expiration,
            args=(),
        ).start()

        try:
            files_listener(config.DIRECTORY_TO_WATCH)
        except Exception as e:
            error_or_success_logger.debug(f"Error in files_listener: {e}")

    except Exception as e:
        error_or_success_logger.debug(f"Error starting file expiration listener: {e}")


if __name__ == "__main__":
    main()
