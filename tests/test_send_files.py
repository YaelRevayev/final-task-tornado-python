import unittest
from unittest.mock import MagicMock, patch
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
sys.path.append(project_dir)
sys.path.insert(0, "./src")
from src.send_files import (
    classifyFiles,
    send_http_request,
)
import src.file_operations as file_operations


class TestMainScript(unittest.TestCase):
    def setUp(self):
        self.sender_logger = MagicMock()
        self.error_logger = MagicMock()

    @patch("redis_operations.save_to_redis")
    @patch("redis_operations.does_key_exists", return_value=False)
    @patch("file_operations.remove_extension", return_value="file_name")
    def test_key_not_exists(
        self, mock_remove_extension, mock_does_key_exists, mock_save_to_redis
    ):
        sender_logger_instance = MagicMock()
        error_logger_instance = MagicMock()
        with patch("redis_operations.redis"):
            classifyFiles(
                "curr_filename", sender_logger_instance, error_logger_instance
            )

        mock_does_key_exists.assert_called_once_with("file_name")
        mock_remove_extension.assert_called_once_with("curr_filename")
        mock_save_to_redis.assert_called_once_with("file_name", "curr_filename")

    @patch(
        "send_files.list_files",
        return_value=[("files", ("filename", b"file_content"))],
    )
    @patch("send_files.remove_file_from_os")
    @patch("send_files.send_http_request")
    @patch("redis_operations.get_value_by_key", return_value="first_file_name")
    @patch("redis_operations.does_key_exists", return_value=True)
    @patch("file_operations.remove_extension", return_value="file_name")
    def test_key_exists(
        self,
        mock_remove_extension,
        mock_does_key_exists,
        mock_get_value_by_key,
        mock_send_http_request,
        mock_remove_file_from_os,
        mock_list_files,
    ):
        sender_logger_instance = MagicMock()
        error_logger_instance = MagicMock()
        with patch("redis_operations.redis"):
            classifyFiles(
                "curr_filename", sender_logger_instance, error_logger_instance
            )

        mock_does_key_exists.assert_called_once_with("file_name")
        mock_remove_extension.assert_called_once_with("curr_filename")
        mock_get_value_by_key.assert_called_once_with("file_name")
        mock_list_files.assert_called_once_with("curr_filename", "first_file_name")
        mock_send_http_request.assert_called_once_with(
            "curr_filename",
            "first_file_name",
            [("files", ("filename", b"file_content"))],
        )
        mock_remove_file_from_os.assert_called_once_with(
            "directory_to_watch", "first_file_name"
        )
        mock_remove_file_from_os.assert_called_once_with(
            "directory_to_watch", "curr_filename"
        )


@patch("send_files.requests.post")
def test_send_http_request_success(self, mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    mock_sender_logger = MagicMock()
    mock_error_logger = MagicMock()

    send_http_request(
        "filename", "first_file_name", [("files", ("filename", b"file_content"))]
    )

    mock_sender_logger.info.assert_called_once_with(
        "Files 'first_file_name' , 'filename' sent successfully."
    )
    mock_error_logger.error.assert_not_called()


@patch("send_files.requests.post")
def test_send_http_request_failure(self, mock_post):
    mock_response = MagicMock(status_code=404, reason="Not Found")
    mock_post.return_value = mock_response

    mock_sender_logger = MagicMock()
    mock_error_logger = MagicMock()

    send_http_request("filename", "first_file_name", [])

    mock_error_logger.error.assert_called_once_with(
        "Error sending files 'first_file_name' , 'filename': 404 Not Found"
    )
    mock_sender_logger.info.assert_not_called()


if __name__ == "__main__":

    unittest.main()
