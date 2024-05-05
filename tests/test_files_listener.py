import unittest
from unittest.mock import MagicMock, patch
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)
from src.files_listener import NewFileHandler, start_watchdog
from src.send_files import classifyFiles


class TestNewFileHandler(unittest.TestCase):

    @patch("files_listener.threading.Thread")
    def test_on_created(self, mock_thread):
        mock_sender_logger = MagicMock()
        mock_error_logger = MagicMock()
        mock_watchdog_logger = MagicMock()

        handler = NewFileHandler(
            mock_sender_logger, mock_error_logger, mock_watchdog_logger
        )
        mock_event = MagicMock()
        mock_event.src_path = "image01_a.jpg"
        mock_event.is_directory = False

        handler.on_created(mock_event)

        mock_watchdog_logger.info.assert_called_once_with(
            "New file detected: image01_a.jpg"
        )
        mock_thread.assert_called_once_with(
            target=classifyFiles,
            args=(
                mock_event.src_path,
                mock_sender_logger,
                mock_error_logger,
            ),
        )
        result = mock_thread.return_value.start.assert_called_once()

    @patch("files_listener.Observer")
    def test_start_watchdog(self, mock_observer):
        mock_sender_logger = MagicMock()
        mock_error_logger = MagicMock()
        mock_watchdog_logger = MagicMock()

        directory = "files_output"
        start_watchdog(
            directory,
            mock_sender_logger,
            mock_error_logger,
            mock_watchdog_logger,
            run_indefinitely=False,
        )

        mock_observer_instance = mock_observer.return_value
        mock_observer_instance.start.assert_called_once()
        mock_watchdog_logger.info.assert_called_once_with(
            f"Watching directory: {directory}"
        )


if __name__ == "__main__":
    unittest.main()
