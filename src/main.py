from files_listener import files_listener, listen_for_file_expiration
import configs.config as config


def main():
    listen_for_file_expiration()
    files_listener(config.DIRECTORY_TO_WATCH)


if __name__ == "__main__":
    main()
