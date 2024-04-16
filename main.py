from files_listener import files_listener
from send_files import listen_for_redis_keys_expiration
import config
import threading
from file_operations import reset_folder


if __name__ == "__main__":
    reset_folder(config.LOGS_FOLDER_NAME)
    reset_folder(config.FILES_FOLDER_NAME)
    threading.Thread(target=listen_for_redis_keys_expiration).start()
    files_listener(config.DIRECTORY_TO_WATCH)
