import os


def read_file(filename):
    with open(filename, "rb") as file:
        file_data = file.read()

    return file_data


def remove_extension(filename):
    base_filename, _ = os.path.splitext(filename)
    return base_filename
