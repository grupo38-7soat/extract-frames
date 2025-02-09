import unittest
from unittest.mock import patch, MagicMock
import json
from src.app import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('src.app.SagaControl')
    def test_lambda_handler(self, MockSagaControl):
        mock_saga_instance = MockSagaControl.return_value
        mock_saga_instance.run.return_value = None

        event = {
            "Records": [{
                "messageId": "ceeeb811-a50d-43eb-a0ad-595e6467afb6",
                "receiptHandle": "AQEBJTfWu49dGfKhhK1aR7ca854Sb20F/Y7k0VKTB6G4Gdtgm7e2kTgyXSTfKavvVJmybYjTjE2Qn+1LdnAfHr5QCFNq5pHxvPNmC4gnvginWR/tkgGGo3O+qQaGYHnPrYoyhhFIIFkxRelIJ75clPrZkWV4g2xADRYLwESfwNPTrMjaKoY+E0zVGpl0G5cbNf14m3u6B61mDxgR9VSDClPz9b7wA9TnD9IBnGxJlJs71g0iJ1SWbWpQ+r22dpyZTMhWYeicP4yqUsM8xPUkExi4YQadZNmmwFj3xTutBjrj7yRH2cXyUX4AqdPPV+5gt2TTGuAlJpyziTa0sCUi2vZe97+0Piv8wo1HGBAg34rG0OzCY7hdIGk5/8m6xsortmqujn6ujTPWkbOtwd5JFCm3bw==",
                "body": json.dumps({
                    "user": "novo_user_1",
                    "video_name": "SampleVideo_1280x720_1mb.mp4",
                    "start_time_for_cut_frames": 0,
                    "end_time_for_cut_frames": 0,
                    "skip_frame": 1
                }),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1739057437791",
                    "SenderId": "940482415113",
                    "ApproximateFirstReceiveTimestamp": "1739057437802"
                },
                "messageAttributes": {},
                "md5OfBody": "e721e55644c6e771070575775182d80a",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:940482415113:extract-frames-queue",
                "awsRegion": "us-east-1"
            }]
        }

        lambda_handler(event, None)

        MockSagaControl.assert_called_once_with({
            "user": "novo_user_1",
            "video_name": "SampleVideo_1280x720_1mb.mp4",
            "start_time_for_cut_frames": 0,
            "end_time_for_cut_frames": 0,
            "skip_frame": 1
        })
        mock_saga_instance.run.assert_called_once()

    @patch('src.app.SagaControl')
    def test_lambda_handler_exception(self, MockSagaControl):
        mock_saga_instance = MockSagaControl.return_value
        mock_saga_instance.run.side_effect = Exception("Test exception")

        event = {
            "Records": [{
                "messageId": "ceeeb811-a50d-43eb-a0ad-595e6467afb6",
                "receiptHandle": "AQEBJTfWu49dGfKhhK1aR7ca854Sb20F/Y7k0VKTB6G4Gdtgm7e2kTgyXSTfKavvVJmybYjTjE2Qn+1LdnAfHr5QCFNq5pHxvPNmC4gnvginWR/tkgGGo3O+qQaGYHnPrYoyhhFIIFkxRelIJ75clPrZkWV4g2xADRYLwESfwNPTrMjaKoY+E0zVGpl0G5cbNf14m3u6B61mDxgR9VSDClPz9b7wA9TnD9IBnGxJlJs71g0iJ1SWbWpQ+r22dpyZTMhWYeicP4yqUsM8xPUkExi4YQadZNmmwFj3xTutBjrj7yRH2cXyUX4AqdPPV+5gt2TTGuAlJpyziTa0sCUi2vZe97+0Piv8wo1HGBAg34rG0OzCY7hdIGk5/8m6xsortmqujn6ujTPWkbOtwd5JFCm3bw==",
                "body": json.dumps({
                    "user": "novo_user_1",
                    "video_name": "SampleVideo_1280x720_1mb.mp4",
                    "start_time_for_cut_frames": 0,
                    "end_time_for_cut_frames": 0,
                    "skip_frame": 1
                }),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1739057437791",
                    "SenderId": "940482415113",
                    "ApproximateFirstReceiveTimestamp": "1739057437802"
                },
                "messageAttributes": {},
                "md5OfBody": "e721e55644c6e771070575775182d80a",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:940482415113:extract-frames-queue",
                "awsRegion": "us-east-1"
            }]
        }

        with self.assertRaises(Exception) as context:
            lambda_handler(event, None)

        self.assertEqual(str(context.exception), "Test exception")

if __name__ == '__main__':
    unittest.main()