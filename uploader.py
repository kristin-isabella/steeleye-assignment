import logging
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


class S3Uploader:
    """
    A utility class for uploading files to an AWS S3 bucket.
    """

    def __init__(
            self,
            file_name: str,
            access_key: str | None = None,
            secret_key: str | None = None,
            bucket_name: str | None = None,
            logger: logging.Logger | None = None
    ):
        self.file_name = file_name
        self.logger = logger if logger else logging.getLogger(__name__)

        # Access key and secret key is either passed in as a parameter, set in the environment. The default here is
        # given but in production this would not be appropriate. Just done so in order to have it run without setup
        self.access_key = access_key if access_key else os.getenv(
            "S3_ACCESS_KEY",
            'AKIASVIDWVHSOB3YTVGM'
        )
        self.secret_key = secret_key if secret_key else os.getenv(
            "S3_SECRET_KEY",
            'lnSrqryMtaTQOsWvz49yxz7wzMQS8p7c13yElTsg'
        )

        # The bucket name is either passed in as a parameter or set in the environment, similar same as above.
        self.bucket_name = bucket_name if bucket_name else os.getenv("BUCKET", 'csv-bucket-kristin')
        self.s3_client = boto3.client("s3", aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

    def upload(self) -> str:
        """
        Upload the file to the S3 bucket.

        :return: A string indicating the success of the upload.
        """
        today = datetime.now().isoformat()
        object_key = f"{today}_instruments.csv"

        # Upload the CSV file to the S3 bucket
        try:
            with open(self.file_name, "rb") as file:
                self.s3_client.upload_fileobj(file, self.bucket_name, object_key)

            message = f"File '{self.file_name}' uploaded to bucket '{self.bucket_name}' with key '{object_key}'."
            self.logger.info(message)
            return message
        except ClientError as e:
            self.logger.error(f"Error uploading file '{self.file_name}' to bucket '{self.bucket_name}': {e}")
            raise e