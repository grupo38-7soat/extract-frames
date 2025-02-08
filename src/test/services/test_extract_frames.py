import pytest
import os
import imageio
from src.services.extract_frames import ExtractFrames
from unittest.mock import patch, MagicMock

@pytest.fixture
def video_path(tmp_path):
    video_file = tmp_path / "test_video.mp4"
    writer = imageio.get_writer(str(video_file), fps=10)
    for i in range(30):
        writer.append_data((i * 10) * 255 * 3 * 3)
    writer.close()
    return str(video_file)

@pytest.fixture
def extract_frames():
    return ExtractFrames(start_time=0, end_time=3, frame_skip=1)

def test_calculate_frame():
    assert ExtractFrames._ExtractFrames__calculate_frame(2, 10) == 20

def test_valid_attributes(extract_frames):
    extract_frames._ExtractFrames__valid_attributes(5)
    assert extract_frames.end_time == 3

def test_file_name():
    assert ExtractFrames._ExtractFrames__file_name(1) == "frame_1.png"