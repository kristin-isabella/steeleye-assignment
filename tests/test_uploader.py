import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile

from uploader import S3Uploader


class TestS3Uploader(unittest.TestCase):

    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.test_file.write("Test data")
        self.test_file.flush()

    def tearDown(self):
        os.remove(self.test_file.name)

    @patch("uploader.boto3.client")
    def test_upload(self, mock_boto3_client):
        mock_upload_fileobj = MagicMock()
        mock_boto3_client.return_value.upload_fileobj = mock_upload_fileobj

        uploader = S3Uploader(file_name=self.test_file.name)
        uploader.upload()

        mock_upload_fileobj.assert_called_once()

    @patch("uploader.boto3.client")
    def test_upload_with_error(self, mock_boto3_client):
        mock_boto3_client.return_value.upload_fileobj.side_effect = Exception("Error uploading")

        uploader = S3Uploader(file_name=self.test_file.name)
        with self.assertRaises(Exception):
            uploader.upload()
