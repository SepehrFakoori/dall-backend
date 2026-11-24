from contextlib import closing
from dataclasses import dataclass

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


@dataclass(frozen=True)
class StoredObject:
    key: str
    version_id: str
    size_bytes: int
    content_type: str


class S3Storage:
    def __init__(self, client, *, bucket: str):
        self._client = client
        self._bucket = bucket

    @classmethod
    def from_aws(cls, *, bucket: str, region: str) -> "S3Storage":
        client = boto3.client(
            "s3",
            region_name=region,
            config=Config(
                signature_version="s3v4",
                s3={
                    "addressing_style": "virtual"
                },  # path: example.com/bucket | virtual: bucket.example.com/
            ),
        )
        return cls(client, bucket=bucket)
