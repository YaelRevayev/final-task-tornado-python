from src.files_listener import files_listener, listen_for_file_expiration
import config.config as config
import threading


def main():
    threading.Thread(
        target=listen_for_file_expiration,
        args=(),
    ).start()
    files_listener(config.DIRECTORY_TO_WATCH)


if __name__ == "__main__":
    main()
