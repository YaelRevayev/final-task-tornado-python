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
from src.send_files import classifyFiles


class TestFileListener(unittest.TestCase):

    @patch("src.files_listener.sender_logger")
    @patch("src.files_listener.error_logger")
    @patch("src.files_listener.watchdog_logger")
    @patch("src.files_listener.multiprocessing.Process")
    def test_on_created(
        self, mock_process, mock_watchdog_logger, mock_error_logger, mock_sender_logger
    ):
        event = MagicMock()
        event.is_directory = False
        event.src_path = "/path/to/file.txt"

        handler = NewFileHandler()
        mock_watchdog_logger.info.assert_called_once_with("New file detected: file.txt")

        mock_process.assert_called_once_with(
            target=handler.classify_files,
            args=(event.src_path, mock_sender_logger, mock_error_logger),
        )

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
    @patch("src.files_listener.create_loggers")
    def test_scan_directory(self, mock_create_loggers, mock_process, mock_listdir):
        sender_logger = MagicMock()
        error_logger = MagicMock()
        watchdog_logger = MagicMock()
        watchdog_logger.info = MagicMock()
        watchdog_logger.info = MagicMock()

        mock_create_loggers.return_value = (
            sender_logger,
            watchdog_logger,
            error_logger,
        )

        directory = "/path/to/directory"
        mock_listdir.return_value = ["file1.txt", "file2.txt"]

        scan_directory(directory)

        mock_listdir.assert_called_once_with(directory)
        self.assertEqual(mock_process.call_count, 2)
        mock_process.assert_any_call(
            target=classifyFiles, args=("file1.txt", sender_logger, error_logger)
        )
        mock_process.assert_any_call(
            target=classifyFiles, args=("file2.txt", sender_logger, error_logger)
        )


if __name__ == "__main__":
    unittest.main()
