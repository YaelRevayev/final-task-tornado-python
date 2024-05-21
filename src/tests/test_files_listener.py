import unittest
from unittest.mock import MagicMock, patch, call
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from files_listener import NewFileHandler, scan_directory


class TestFileListener(unittest.TestCase):

    @patch("files_listener.detected_files_logger")
    @patch("files_listener.multiprocessing.Process")
    def test_on_created_mocking_creation_of_one_file_logger_should_be_called_once(
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

    @patch("files_listener.os.listdir")
    @patch("files_listener.detected_files_logger")
    @patch("files_listener.multiprocessing.Process")
    @patch("files_listener.classifyFiles")
    def test_scan_directory_mocking_three_files_should_open_two_processes(
        self, mock_classifyFiles, MockProcess, mock_logger, mock_listdir
    ):
        mock_listdir.return_value = ["file1_a.jpg", "file2_b", ".gitkeep"]

        directory = "/path/to/directory"
        scan_directory(directory)

        mock_listdir.assert_called_once_with(directory)

        expected_log_calls = [
            call.info("Detected file: file1_a.jpg"),
            call.info("Detected file: file2_b"),
        ]
        mock_logger.info.assert_has_calls(expected_log_calls, any_order=True)

        expected_process_calls = [
            call(target=mock_classifyFiles, args=(f"{directory}/file1_a.jpg",)),
            call(target=mock_classifyFiles, args=(f"{directory}/file2_b",)),
        ]
        MockProcess.assert_has_calls(expected_process_calls, any_order=True)
        self.assertEqual(MockProcess.return_value.start.call_count, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
