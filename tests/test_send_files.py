import unittest
from unittest.mock import MagicMock, patch
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
from src.send_files import (
    classifyFiles,
    part_a_or_b,
    list_files_in_order,
    send_http_request,
)


class TestMainScript(unittest.TestCase):

    @patch("send_files.redis_client.exists")
    @patch("send_files.save_to_redis")
    def test_classifyFiles_key_does_not_exist(
        self, mock_save_to_redis, mock_redis_exists
    ):
        mock_redis_exists.return_value = False

        sender_logger = MagicMock()
        error_logger = MagicMock()
        curr_filename = "files_output/image100_a.jpg"

        classifyFiles(curr_filename, sender_logger, error_logger)
        mock_save_to_redis.assert_called_once_with("image100", "image100_a.jpg")

    @patch("send_files.redis_client.exists")
    @patch("send_files.redis_client.get")
    @patch("send_files.list_files_in_order")
    @patch("send_files.send_http_request")
    @patch("os.remove")
    def test_classifyFiles_key_exists(
        self,
        mock_os_remove,
        mock_send_http_request,
        mock_list_files_in_order,
        mock_redis_get,
        mock_redis_exists,
    ):
        mock_redis_exists.return_value = True
        mock_redis_get.return_value.decode.return_value = "image100_a.jpg"

        sender_logger = MagicMock()
        error_logger = MagicMock()
        curr_filename = "files_output/image100_b"

        classifyFiles(curr_filename, sender_logger, error_logger)
        mock_list_files_in_order.assert_called_once_with("image100_b", "image100_a.jpg")
        mock_send_http_request.assert_called_once()

    def test_part_a_or_b_a(self):
        filename = "filename_a.txt"
        self.assertEqual(part_a_or_b(filename), "a")

    def test_part_a_or_b_b(self):
        filename = "filename_b"
        self.assertEqual(part_a_or_b(filename), "b")

    def test_part_a_or_b_none(self):
        filename = "filename.txt"
        self.assertIsNone(part_a_or_b(filename))

    def test_list_files_in_order(self):
        with patch("send_files.read_file") as mock_read_file:
            mock_read_file.return_value = b"file content"
            result = list_files_in_order("file_b.txt", "file_a.txt")
            expected_result = [
                ("files", ("file_a.txt", b"file content")),
                ("files", ("file_b.txt", b"file content")),
            ]
            self.assertEqual(result, expected_result)

    @patch("send_files.requests.post")
    def test_send_http_request_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        mock_sender_logger = MagicMock()
        mock_error_logger = MagicMock()

        send_http_request(
            "filename",
            "first_file_name",
            [("files", ("filename", b"file_content"))],
            mock_sender_logger,
            mock_error_logger,
        )

        mock_sender_logger.info.assert_called_once_with(
            "Files 'first_file_name' , 'filename' sent successfully."
        )

    @patch("send_files.requests.post")
    def test_send_http_request_failure(self, mock_post):
        mock_response = MagicMock(status_code=404, reason="Not Found")
        mock_post.return_value = mock_response

        mock_sender_logger = MagicMock()
        mock_error_logger = MagicMock()

        send_http_request(
            "filename", "first_file_name", [], mock_sender_logger, mock_error_logger
        )

        mock_error_logger.error.assert_called_once_with(
            "Error sending files 'first_file_name' , 'filename': 404 Not Found"
        )


if __name__ == "__main__":

    unittest.main()
