import unittest
from unittest.mock import MagicMock, patch
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
sys.path.insert(0, "./src")
from src.files_listener import (
    NewFileHandler,
    start_watchdog,
    scan_directory,
)
from src.send_files import *


class TestFileListener(unittest.TestCase):
    def setUp(self):
        self.sender_logger = MagicMock()
        self.watchdog_logger = MagicMock()
        self.watchdog_logger.info = MagicMock()
        self.error_logger = MagicMock()

    @patch("src.files_listener.sender_logger")
    @patch("src.files_listener.error_logger")  #
    @patch("src.files_listener.watchdog_logger")
    @patch("src.files_listener.multiprocessing.Process")
    def test_on_created(
        self, mock_process, mock_watchdog_logger, mock_error_logger, mock_sender_logger
    ):
        event = MagicMock()
        event.is_directory = False
        event.src_path = "/path/to/file.txt"

        handler = NewFileHandler()
        handler.on_created(event)
        mock_watchdog_logger.info.assert_called_once_with("New file detected: file.txt")

    @patch("src.files_listener.Observer")
    def test_start_watchdog(self, mock_observer):

        directory = "/path/to/directory"
        run_indefinitely = False

        start_watchdog(directory, run_indefinitely)

        mock_observer_instance = mock_observer.return_value
        mock_observer_instance.schedule.assert_called_once()
        expected_handler = NewFileHandler()
        actual_handler = mock_observer_instance.schedule.call_args[0][0]
        self.assertEqual(expected_handler.__class__, actual_handler.__class__)

    @patch("src.files_listener.os.listdir")
    @patch("src.files_listener.multiprocessing.Process")
    def test_scan_directory(self, mock_process, mock_listdir):

        directory = "/path/to/directory"
        mock_listdir.return_value = ["file1.txt", "file2.txt"]
        scan_directory(directory)

        mock_listdir.assert_called_once_with(directory)
        self.assertEqual(mock_process.call_count, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
