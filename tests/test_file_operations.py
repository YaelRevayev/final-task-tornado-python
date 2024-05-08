import unittest
from unittest.mock import patch
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
sys.path.insert(0, "./src")
from src.file_operations import read_file, remove_extension


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


if __name__ == "__main__":
    unittest.main()
