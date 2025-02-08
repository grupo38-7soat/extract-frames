# test_app.py
import pytest
from unittest.mock import patch, MagicMock
from src.app import lambda_handler

@pytest.fixture
def event():
    return {
        "user": "123",
        "video_name": "SampleVideo_1280x720_1mb.mp4",
        "start_time_for_cut_frames": 0,
        "end_time_for_cut_frames": 0,
        "skip_frame": 1
    }

@patch('src.app.SagaControl')
def test_lambda_handler_success(mock_saga_control, event):
    mock_saga_control.return_value.run = MagicMock()
    lambda_handler(event, None)
    mock_saga_control.assert_called_once_with(event)
    mock_saga_control.return_value.run.assert_called_once()

@patch('src.app.SagaControl')
def test_lambda_handler_exception(mock_saga_control, event):
    mock_saga_control.return_value.run.side_effect = Exception("Test exception")
    with pytest.raises(Exception, match="Test exception"):
        lambda_handler(event, None)