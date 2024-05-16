import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from files_listener import NewFileHandler, start_watchdog, scan_directory


class TestFileListener(unittest.TestCase):

    @patch("logger.detected_files_logger")
    @patch("files_listener.multiprocessing.Process")
    def test_on_created_mocking_creation_of_one_file_logger_called_once(
        self,
        mock_process,
        mock_detected_files_logger,
    ):
        event = MagicMock()
        event.is_directory = False
        event.src_path = "/path/to/file.txt"

        handler = NewFileHandler()
        handler.on_created(event)
        mock_detected_files_logger.info.assert_called_once_with(
            "New file detected: file.txt"
        )

    @patch("files_listener.Observer")
    def test_start_watchdog_giving_nothing_asserting_functions_called(
        self, mock_observer
    ):

        directory = "/path/to/directory"
        run_indefinitely = False

        start_watchdog(directory, run_indefinitely)

        mock_observer_instance = mock_observer.return_value
        mock_observer_instance.schedule.assert_called_once()
        expected_handler = NewFileHandler()
        actual_handler = mock_observer_instance.schedule.call_args[0][0]
        self.assertEqual(expected_handler.__class__, actual_handler.__class__)

    @patch("files_listener.os.listdir")
    @patch("files_listener.multiprocessing.Process")
    def test_scan_directory_mocking_2_files_called_twice(
        self, mock_process, mock_listdir
    ):

        directory = "/path/to/directory"
        mock_listdir.return_value = ["file1.txt", "file2.txt"]
        scan_directory(directory)

        mock_listdir.assert_called_once_with(directory)
        self.assertEqual(mock_process.call_count, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)