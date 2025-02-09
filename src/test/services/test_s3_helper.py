import unittest
from unittest.mock import patch, MagicMock, mock_open
from services.s3_helper import S3Helper
from constants.constant_env import BUCKET_NAME, DOWNLOAD_FOLDER_NAME


class TestS3Helper(unittest.TestCase):
    @patch("boto3.client")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_s3_stream_error(self, mock_file, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client

        mock_s3_client.get_object.side_effect = Exception("Erro ao baixar o arquivo")

        file_name = "test.mp4"
        temp_video_path = "/tmp/test.mp4"

        s3_helper = S3Helper()

        with self.assertRaises(Exception) as context:
            s3_helper.download_s3_stream(file_name, temp_video_path)

        self.assertEqual(str(context.exception), "Erro ao baixar o arquivo")

    @patch("boto3.client")
    def test_upload_file_to_s3_success(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client

        local_path = "/tmp/test.mp4"
        result = "uploaded/test.mp4"

        s3_helper = S3Helper()

        s3_helper.upload_file_to_s3(local_path, result)

        mock_s3_client.upload_file.assert_called_once_with(local_path, BUCKET_NAME, result)

    @patch("boto3.client")
    def test_upload_file_to_s3_error(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client

        mock_s3_client.upload_file.side_effect = Exception("Erro ao fazer upload")

        local_path = "/tmp/test.mp4"
        result = "uploaded/test.mp4"

        s3_helper = S3Helper()

        with self.assertRaises(Exception) as context:
            s3_helper.upload_file_to_s3(local_path, result)

        self.assertEqual(str(context.exception), "Erro ao fazer upload")


if __name__ == "__main__":
    unittest.main()
