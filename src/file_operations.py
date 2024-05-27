import os
from configs import config as config
from logger import error_or_success_logger

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def read_file(filename: str) -> bytes:
    error_or_success_logger.debug("reading file...")
    try:
        with open(f"/{project_dir}/{filename}", "rb") as file:
            file_data = file.read()
        error_or_success_logger.debug(f"{filename} --> {file_data}")

        return file_data
    except Exception as e:
        error_or_success_logger.error(f"Exception occurred: {e}")


def remove_extension(filename: str) -> str:
    base_filename, _ = os.path.splitext(filename)
    return base_filename


def remove_files_from_os(*filenames):
    for filename in filenames:
        os.remove((f"{config.DIRECTORY_TO_WATCH}/{filename}"))


def list_files_by_request_format(curr_file: str, first_file: str) -> list:
    files_to_send = []
    files_to_send.append(
        ("files", (curr_file, read_file(f"{config.FILES_FOLDER_NAME}/{curr_file}")))
    )
    files_to_send.append(
        ("files", (first_file, read_file(f"{config.FILES_FOLDER_NAME}/{first_file}")))
    )
    error_or_success_logger.debug("listed files...")
    return files_to_send
