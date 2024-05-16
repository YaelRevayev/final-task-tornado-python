import unittest
from unittest.mock import patch, MagicMock
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
sys.path.insert(0, "./src")
from src.file_operations import (
    read_file,
    remove_extension,
    remove_file_from_os,
    list_files,
)


class TestFileFunctions(unittest.TestCase):
    @patch("builtins.open", create=True)
    def test_read_file_with_mocking_file_and_content_returns_mocked_content(
        self, mock_open
    ):
        filename = "test_file.txt"
        mock_open.return_value.__enter__.return_value.read.return_value = b"test_data"
        file_data = read_file(filename)
        self.assertEqual(file_data, b"test_data")

    def test_remove_extension_with_mocking_filename_returns_valid_extension(self):
        filename = "image100_a.jpg"
        base_filename = remove_extension(filename)
        self.assertEqual(base_filename, "image100_a")

    @patch("os.remove")
    def test_remove_file_from_os_with_mocking_file_asserting_function_called_once_with_file(
        self, mock_os_remove
    ):
        folder_name = "test_folder"
        file_name = "test_file.txt"
        remove_file_from_os(folder_name, file_name)
        mock_os_remove.assert_called_once_with("test_folder/test_file.txt")

    @patch("builtins.open", new_callable=MagicMock)
    def test_list_files_with_mocking_file_objects_adds_them_to_list(self, mock_open):
        curr_file = "test_curr_file.txt"
        first_file = "test_first_file.txt"
        expected_content_curr = b"ontent_for_test_curr_file.txt"
        expected_content_first = b"content_for_test_first_file.txt"
        mock_curr_file = MagicMock()
        mock_curr_file.__enter__().read.return_value = expected_content_curr
        mock_first_file = MagicMock()
        mock_first_file.__enter__().read.return_value = expected_content_first
        mock_open.side_effect = [mock_curr_file, mock_first_file]
        result = list_files(curr_file, first_file)
        expected_result = [
            ("files", (curr_file, expected_content_curr)),
            ("files", (first_file, expected_content_first)),
        ]
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
