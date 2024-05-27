import unittest
from unittest.mock import MagicMock, patch, call
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from send_files import (
    classifyFiles,
    send_http_request,
    get_storage,
    handle_existing_key,
)
from file_operations import remove_extension, remove_files_from_os
from configs import config as config


class TestSendFiles(unittest.TestCase):

    @patch("send_files.get_storage")
    @patch("send_files.remove_extension", return_value="image100_a")
    @patch("send_files.application_info_logger", return_value=MagicMock())
    def test_classify_files_no_key_exists(
        self, mock_application_info_logger, mock_remove_extension, mock_get_storage
    ):
        mock_storage = MagicMock()
        mock_storage.save.return_value = True
        mock_get_storage.return_value = mock_storage

        classifyFiles("image100_a.jpg")

        mock_remove_extension.assert_called_once_with("image100_a.jpg")
        mock_storage.save.assert_called_once_with("image100", "image100_a.jpg")
        mock_application_info_logger.debug.assert_any_call(
            "opened new process for image100_a.jpg"
        )
        mock_application_info_logger.debug.assert_any_call("no key exists, key saved")

    @patch("send_files.get_storage")
    @patch("send_files.remove_extension", return_value="image100_a")
    @patch("send_files.handle_existing_key")
    @patch("send_files.application_info_logger")
    def test_classify_files_key_exists(
        self,
        mock_application_info_logger,
        mock_handle_existing_key,
        mock_remove_extension,
        mock_get_storage,
    ):
        mock_storage = MagicMock()
        mock_get_storage.return_value = mock_storage

        mock_get_storage.save.return_value = False
        mock_storage.save.return_value = False

        classifyFiles("image100_a.jpg")

        expected_calls = [
            call("opened new process for image100_a.jpg"),
        ]

        mock_storage.save.assert_called_once_with("image100", "image100_a.jpg")
        mock_application_info_logger.debug.assert_has_calls(expected_calls)

        mock_remove_extension.assert_called_once_with("image100_a.jpg")
        mock_handle_existing_key.assert_called_once_with(
            mock_storage, "image100", "image100_a.jpg"
        )

        self.assertTrue(mock_application_info_logger.debug.called)

    @patch("send_files.error_or_success_logger")
    @patch("send_files.session.post")
    def test_send_http_request_success(self, mock_post, mock_error_success_logger):
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
    @patch("send_files.session.post")
    def test_send_http_request_failure(self, mock_post, mock_error_success_logger):
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

    @patch(
        "send_files.list_files_by_request_format",
        return_value=[
            ("files", ("image100_a.jpg", b"file_content1")),
            ("files", ("image100_b", b"file_content2")),
        ],
    )
    @patch("send_files.application_info_logger")
    @patch("send_files.remove_files_from_os")
    def test_handle_existing_key(
        self, mock_remove_file_from_os, mock_application_info_logger, mock_send_files
    ):
        mock_storage = MagicMock()
        mock_storage.get.return_value = "image100_b"

        handle_existing_key(mock_storage, "image100", "image100_a.jpg")

        mock_storage.get.assert_called_once_with("image100")
        mock_remove_file_from_os.assert_called_once_with("image100_b", "image100_a.jpg")
        mock_application_info_logger.debug.assert_called_once_with("key does exists")


if __name__ == "__main__":
    unittest.main(verbosity=2)
