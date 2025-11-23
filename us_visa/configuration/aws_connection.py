import boto3
import os
from us_visa.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME


class S3Client:

    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):

        # Create singleton objects only once
        if S3Client.s3_resource is None or S3Client.s3_client is None:

            # FIX: Strip whitespace and newlines
            __access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY, "").strip()
            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY, "").strip()

            if not __access_key_id:
                raise Exception(f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not set.")
            if not __secret_access_key:
                raise Exception(f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set.")

            # Create S3 resource and client
            S3Client.s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )

            S3Client.s3_client = boto3.client(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )

        # Assign to instance
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client
