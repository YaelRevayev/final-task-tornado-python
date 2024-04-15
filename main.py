from files_listener import files_listener
from logger import reset_folder
import config

if __name__ == "__main__":
    reset_folder(config.LOGS_FOLDER_NAME)
    reset_folder(config.FILES_FOLDER_NAME)
    files_listener(config.DIRECTORY_TO_WATCH)
