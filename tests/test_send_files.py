import unittest
from unittest.mock import MagicMock, patch, call
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
sys.path.append(project_dir)
sys.path.insert(0, "./src")
from src.send_files import classifyFiles, send_http_request
import src.file_operations
import src.redis_operations


class TestMainScript(unittest.TestCase):
    def setUp(self):
        self.sender_logger = MagicMock()
        self.error_logger = MagicMock()

    @patch("src.send_files.save_to_redis", return_value=MagicMock())
    @patch("src.send_files.does_key_exists", return_value=False)
    @patch("redis_operations.redis_client", return_value=MagicMock())
    @patch("src.send_files.remove_extension", return_value="image100_a")
    def test_classify_files_mocked_no_key_exists_creates_redis_key(
        self,
        mock_remove_extension,
        mock_redis_client,
        mock_does_key_exists,
        mock_save_to_redis,
    ):

        classifyFiles(
            "image100_a.jpg",
            self.sender_logger,
            self.error_logger,
        )

        mock_remove_extension.assert_called_with("image100_a.jpg")
        mock_does_key_exists.assert_called_once_with("image100")
        mock_save_to_redis.assert_called_once_with("image100", "image100_a.jpg")

    @patch("src.send_files.does_key_exists", return_value=True)
    @patch("src.send_files.get_value_by_key", return_value="image100_b")
    @patch("redis_operations.redis_client", return_value=MagicMock())
    @patch("src.send_files.remove_extension", return_value="image100_a")
    @patch(
        "src.send_files.list_files",
        return_value=[
            ("files", ("image100_a.jpg", b"file_content1")),
            ("files", ("image100_b", b"file_content2")),
        ],
    )
    @patch("src.send_files.remove_file_from_os")
    @patch("src.send_files.send_http_request", return_value=MagicMock())
    def test_classify_files_mocking_key_exists_asserting_calling_of_different_functions(
        self,
        mock_send_http_request,
        mock_remove_file_from_os,
        mock_list_files,
        mock_remove_extension,
        mock_get_redis_client,
        mock_get_value_by_key,
        mock_does_key_exists,
    ):

        classifyFiles("image100_a.jpg", self.sender_logger, self.error_logger)

        mock_remove_extension.assert_called_once_with("image100_a.jpg")
        mock_does_key_exists.assert_called_once_with("image100")
        mock_get_value_by_key.assert_called_once_with("image100")
        mock_list_files.assert_called_once_with("image100_a.jpg", "image100_b")
        mock_send_http_request.assert_called_with(
            "image100_a.jpg",
            "image100_b",
            [
                ("files", ("image100_a.jpg", b"file_content1")),
                ("files", ("image100_b", b"file_content2")),
            ],
        )
        expected_calls = [
            call("files_output", "image100_b"),
            call("files_output", "image100_a.jpg"),
        ]
        mock_remove_file_from_os.assert_has_calls(expected_calls)

    @patch("src.send_files.sender_logger")
    @patch("src.send_files.error_logger")
    @patch("src.send_files.requests.post")
    def test_send_http_request_sending_valid_list_receiving_success(
        self, mock_post, mock_error_logger, mock_sender_logger
    ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        send_http_request(
            "filename", "first_file_name", [("files", ("filename", b"file_content"))]
        )

        mock_sender_logger.info.assert_called_once_with(
            "Files 'first_file_name' , 'filename' sent successfully."
        )
        mock_error_logger.error.assert_not_called()

    @patch("src.send_files.sender_logger")
    @patch("src.send_files.error_logger")
    @patch("src.send_files.requests.post")
    def test_send_http_request_sending_empty_list_receiving_failure(
        self, mock_post, mock_error_logger, mock_sender_logger
    ):
        mock_response = MagicMock(status_code=404, reason="Not Found")
        mock_post.return_value = mock_response

        send_http_request("filename", "first_file_name", [])

        mock_error_logger.error.assert_called_once_with(
            "Error sending files 'first_file_name' , 'filename': 404 Not Found"
        )
        mock_sender_logger.info.assert_not_called()


if __name__ == "__main__":

    unittest.main()
