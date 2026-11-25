from functools import lru_cache
from urllib.parse import quote

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings


class S3:
    def __init__(
        self,
        *,
        bucket: str,
        region_name: str,
        endpoint_url: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        addressing_style: str = "virtual",
    ):
        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": addressing_style},
            ),
        )

    def generate_presigned_post(
        self,
        *,
        key: str,
        content_type: str,
        max_size: int,
        expires: int = 600,
    ) -> dict:
        return self.client.generate_presigned_post(
            Bucket=self.bucket,
            Key=key,
            Fields={"Content-Type": content_type},
            Conditions=[
                {"Content-Type": content_type},
                ["content-length-range", 1, max_size],
            ],
            ExpiresIn=expires,
        )

    def head_object(self, key: str) -> dict | None:
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=key)
        except ClientError as exc:
            if exc.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
                return None
            raise

        return {
            "size": response["ContentLength"],
            "content_type": response["ContentType"],
        }

    def generate_presigned_get(
        self,
        key: str,
        *,
        expires: int = 300,
        download_name: str | None = None,
    ) -> str:
        params = {"Bucket": self.bucket, "Key": key}
        if download_name:
            params["ResponseContentDisposition"] = (
                f"attachment; filename*=UTF-8''{quote(download_name, safe='')}"
            )
        return self.client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=expires,
        )

    def delete_object(self, key: str) -> None:
        self.client.delete_object(Bucket=self.bucket, Key=key)


@lru_cache(maxsize=1)
def get_s3() -> S3:
    return S3(
        bucket=settings.S3_BUCKET,
        region_name=settings.S3_REGION,
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    )
