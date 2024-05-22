import unittest
from unittest.mock import MagicMock, patch, call
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from send_files import classifyFiles, send_http_request, get_storage
from configs import config


class TestMainScript(unittest.TestCase):

    @patch("send_files.get_storage")
    @patch("send_files.remove_extension", return_value="image100_a")
    @patch("send_files.error_or_success_logger")
    def test_classify_files_mocked_no_key_exists_creates_redis_key(
        self,
        mock_error_or_success_logger,
        mock_remove_extension,
        mock_get_storage,
    ):
        mock_storage = MagicMock()
        mock_storage.exists.return_value = False
        mock_get_storage.return_value = mock_storage

        classifyFiles("image100_a.jpg")

        mock_remove_extension.assert_called_once_with("image100_a.jpg")
        mock_storage.exists.assert_called_once_with("image100")
        mock_storage.save.assert_called_once_with("image100", "image100_a.jpg")
        mock_error_or_success_logger.debug.assert_called_once_with(
            "opened new process for image100_a.jpg"
        )

    @patch("send_files.get_storage")
    @patch("send_files.remove_extension", return_value="image100_a")
    @patch(
        "send_files.list_files",
        return_value=[
            ("files", ("image100_a.jpg", b"file_content1")),
            ("files", ("image100_b", b"file_content2")),
        ],
    )
    @patch("send_files.remove_file_from_os")
    @patch("send_files.send_http_request", return_value=MagicMock())
    @patch("send_files.error_or_success_logger")
    def test_classify_files_mocking_key_exists_asserting_calling_of_different_functions(
        self,
        mock_error_or_success_logger,
        mock_send_http_request,
        mock_remove_file_from_os,
        mock_list_files,
        mock_remove_extension,
        mock_get_storage,
    ):
        mock_storage = MagicMock()
        mock_storage.exists.return_value = True
        mock_storage.get.return_value = "image100_b"
        mock_get_storage.return_value = mock_storage

        classifyFiles("image100_a.jpg")

        mock_remove_extension.assert_called_once_with("image100_a.jpg")
        mock_storage.exists.assert_called_once_with("image100")
        mock_storage.get.assert_called_once_with("image100")
        mock_list_files.assert_called_once_with("image100_a.jpg", "image100_b")
        mock_send_http_request.assert_called_once_with(
            "image100_a.jpg",
            "image100_b",
            [
                ("files", ("image100_a.jpg", b"file_content1")),
                ("files", ("image100_b", b"file_content2")),
            ],
        )
        expected_calls = [
            call(config.DIRECTORY_TO_WATCH, "image100_b"),
            call(config.DIRECTORY_TO_WATCH, "image100_a.jpg"),
        ]
        mock_remove_file_from_os.assert_has_calls(expected_calls)
        mock_error_or_success_logger.debug.assert_called_once_with(
            "opened new process for image100_a.jpg"
        )

    @patch("send_files.error_or_success_logger")
    @patch("send_files.requests.post")
    def test_send_http_request_sending_valid_list_receiving_success(
        self, mock_post, mock_error_success_logger
    ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        send_http_request(
            "filename",
            "first_file_name",
            [
                ("files", ("filename", b"file_content1")),
                ("files", ("first_file_name", b"file_content2")),
            ],
        )

        mock_error_success_logger.info.assert_any_call(
            "File 'first_file_name' sent successfully."
        )
        mock_error_success_logger.info.assert_any_call(
            "File 'filename' sent successfully."
        )
        mock_error_success_logger.error.assert_not_called()

    @patch("send_files.error_or_success_logger")
    @patch("send_files.requests.post")
    def test_send_http_request_sending_empty_list_receiving_failure(
        self, mock_post, mock_error_success_logger
    ):
        mock_response = MagicMock(status_code=404, reason="Not Found")
        mock_post.return_value = mock_response

        send_http_request("filename", "first_file_name", [])

        mock_error_success_logger.error.assert_any_call(
            "Error sending file 'first_file_name': 404 Not Found"
        )
        mock_error_success_logger.error.assert_any_call(
            "Error sending file 'filename': 404 Not Found"
        )
        mock_error_success_logger.info.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
