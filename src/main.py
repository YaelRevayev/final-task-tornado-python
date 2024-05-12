from files_listener import files_listener, listen_for_file_expiration
import configs.config as config
import multiprocessing


def main():
    multiprocessing.Process(
        target=listen_for_file_expiration,
        args=(),
    ).start()
    print("meow")
    files_listener(config.DIRECTORY_TO_WATCH)


if __name__ == "__main__":
    main()
