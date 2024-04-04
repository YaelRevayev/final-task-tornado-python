from files_listener import start_watchdog
from logger import reset_folder

if __name__ == "__main__":
    reset_folder("logs")
    reset_folder("files_output")
    directory_to_watch = "/home/pure-ftpd-server/final-task-tornado-python"
    start_watchdog(directory_to_watch)

