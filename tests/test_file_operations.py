import unittest
from unittest.mock import patch
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
sys.path.insert(0, "./src")
from src.file_operations import read_file, remove_extension, remove_file_from_os


class TestFileFunctions(unittest.TestCase):
    @patch("builtins.open", create=True)
    def test_read_file(self, mock_open):
        filename = "test_file.txt"
        mock_open.return_value.__enter__.return_value.read.return_value = b"test_data"

        file_data = read_file(filename)

        mock_open.assert_called_once_with(filename, "rb")
        self.assertEqual(file_data, b"test_data")

    def test_remove_extension(self):
        filename = "test_file.txt"

        base_filename = remove_extension(filename)

        self.assertEqual(base_filename, "test_file")

    @patch("os.remove")
    def test_remove_file_from_os(self, mock_os_remove):
        folder_name = "test_folder"
        file_name = "test_file.txt"

        remove_file_from_os(folder_name, file_name)

        mock_os_remove.assert_called_once_with("test_folder/test_file.txt")


if __name__ == "__main__":
    unittest.main()
