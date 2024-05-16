import os
import configs as config

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def read_file(filename):
    with open("/{0}/{1}".format(project_dir, filename), "rb") as file:
        file_data = file.read()
    return file_data


def remove_extension(filename):
    base_filename, _ = os.path.splitext(filename)
    return base_filename


def remove_file_from_os(folder_name, file_name):
    os.remove(("{0}/{1}").format(folder_name, file_name))


def list_files(curr_file, first_file):
    files_to_send = []
    files_to_send.append(
        ("files", (curr_file, read_file(f"{config.FILES_FOLDER_NAME}/{curr_file}")))
    )
    files_to_send.append(
        ("files", (first_file, read_file(f"{config.FILES_FOLDER_NAME}/{first_file}")))
    )
    return files_to_send
