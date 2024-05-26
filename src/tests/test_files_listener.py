import unittest
from unittest.mock import MagicMock, patch, call
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from files_listener import NewFileHandler, scan_directory
from send_files import classifyFiles


class TestFileListener(unittest.TestCase):

    @patch("files_listener.detected_files_logger")
    @patch("files_listener.error_or_success_logger")
    @patch("files_listener.Pool")
    def test_on_created_mocking_creation_of_one_file_logger_should_be_called_once(
        self,
        mock_pool,
        mock_error_or_success_logger,
        mock_detected_files_logger,
    ):
        mock_pool_instance = mock_pool.return_value
        event = MagicMock()
        event.is_directory = False
        event.src_path = "/path/to/file.txt"

        handler = NewFileHandler(mock_pool_instance)
        handler.on_closed(event)
        mock_error_or_success_logger.debug.assert_called_once_with(
            "detected new file creation"
        )
        mock_detected_files_logger.info.assert_called_once_with(
            "New file detected: file.txt"
        )
        mock_pool_instance.apply_async.assert_called_once_with(
            classifyFiles, args=("/path/to/file.txt",)
        )

    @patch("files_listener.os.listdir")
    @patch("files_listener.detected_files_logger")
    @patch("files_listener.Pool")
    def test_scan_directory_mocking_2_files_called_twice(
        self, mock_pool, mock_detected_files_logger, mock_listdir
    ):
        mock_pool_instance = mock_pool.return_value
        directory = "/path/to/directory"
        mock_listdir.return_value = ["file1.txt", "file2.txt"]

        scan_directory(directory, mock_pool_instance)

        mock_listdir.assert_called_once_with(directory)
        expected_log_calls = [
            call.info("Detected file: file1.txt"),
            call.info("Detected file: file2.txt"),
        ]
        mock_detected_files_logger.info.assert_has_calls(
            expected_log_calls, any_order=True
        )
        self.assertEqual(mock_pool_instance.apply_async.call_count, 2)

    @patch("files_listener.os.listdir")
    @patch("files_listener.detected_files_logger")
    @patch("files_listener.Pool")
    def test_scan_directory_mocking_three_files_should_open_two_processes(
        self, mock_pool, mock_detected_files_logger, mock_listdir
    ):
        mock_pool_instance = mock_pool.return_value
        mock_listdir.return_value = ["file1_a.jpg", "file2_b", ".gitkeep"]

        directory = "/path/to/directory"
        scan_directory(directory, mock_pool_instance)

        mock_listdir.assert_called_once_with(directory)

        expected_log_calls = [
            call.info("Detected file: file1_a.jpg"),
            call.info("Detected file: file2_b"),
        ]
        mock_detected_files_logger.info.assert_has_calls(
            expected_log_calls, any_order=True
        )

        expected_apply_async_calls = [
            call(classifyFiles, args=(os.path.join(directory, "file1_a.jpg"),)),
            call(classifyFiles, args=(os.path.join(directory, "file2_b"),)),
        ]
        mock_pool_instance.apply_async.assert_has_calls(
            expected_apply_async_calls, any_order=True
        )
        self.assertEqual(mock_pool_instance.apply_async.call_count, 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
