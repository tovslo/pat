"""
Yandex Cloud Object Storage client (S3-compatible).
ref: spec.md → S3-Compatible Storage → aioboto3, Presigned URLs
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError


def _read_secret(name: str, env_fallback: str = "") -> str:
    path = Path(f"/run/secrets/{name}")
    if path.exists():
        return path.read_text().strip()
    return os.getenv(env_fallback, "")


# S3 endpoint: Yandex Cloud в prod, MinIO (http://localhost:9000) в dev
# ref: spec.md → MinIO for Dev / Yandex Cloud for Prod
S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL", "https://storage.yandexcloud.net")
S3_REGION = os.getenv("S3_REGION", "ru-central1")

_S3_CONFIG = Config(
    region_name=S3_REGION,
    s3={"addressing_style": os.getenv("S3_ADDRESSING_STYLE", "path")},
    signature_version="s3v4",
    retries={"max_attempts": 3, "mode": "adaptive"},
)

_session = aioboto3.Session(
    aws_access_key_id=_read_secret("s3_access_key", "S3_ACCESS_KEY"),
    aws_secret_access_key=_read_secret("s3_secret_key", "S3_SECRET_KEY"),
)

BUCKET = os.getenv("S3_BUCKET_NAME", "myapp-production")


@asynccontextmanager
async def s3_client() -> AsyncGenerator:
    """Async context manager — yields a configured S3 client for Yandex Cloud."""
    async with _session.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        config=_S3_CONFIG,
    ) as client:
        yield client


async def generate_presigned_upload(
    file_key: str,
    content_type: str,
    expires_in: int = 900,  # 15 min
) -> dict[str, str]:
    """
    Generate a presigned PUT URL for direct browser-to-S3 upload.
    ref: spec.md → Presigned URL Upload/Download (Zero-backend bandwidth)
    """
    async with s3_client() as s3:
        url = await s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET,
                "Key": file_key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )
    return {"upload_url": url, "file_key": file_key}


async def generate_presigned_download(
    file_key: str,
    expires_in: int = 3600,
) -> str:
    """
    Generate a presigned GET URL for secure file download.
    ref: spec.md → Presigned URL Upload/Download
    """
    async with s3_client() as s3:
        return await s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET, "Key": file_key},
            ExpiresIn=expires_in,
        )


async def delete_object(file_key: str) -> None:
    """
    Delete a single object. Called by Celery file tasks on completion/failure.
    ref: spec.md → files: auto-cleanup on completion/failure
    """
    async with s3_client() as s3:
        try:
            await s3.delete_object(Bucket=BUCKET, Key=file_key)
        except ClientError:
            pass  # already deleted or never existed — safe to ignore


async def set_lifecycle_policy() -> None:
    """
    Apply S3 lifecycle rules.
    ref: spec.md → Object Lifecycle Policies
      - Delete temp/draft files after 24h (prefix: tmp/)
      - Archive reports after 90 days (prefix: reports/)
    Run once during infra setup, not on every deploy.
    """
    async with s3_client() as s3:
        await s3.put_bucket_lifecycle_configuration(
            Bucket=BUCKET,
            LifecycleConfiguration={
                "Rules": [
                    {
                        "ID": "delete-temp-files-24h",
                        "Status": "Enabled",
                        "Filter": {"Prefix": "tmp/"},
                        "Expiration": {"Days": 1},
                    },
                    {
                        "ID": "archive-reports-90d",
                        "Status": "Enabled",
                        "Filter": {"Prefix": "reports/"},
                        "Expiration": {"Days": 90},
                    },
                ]
            },
        )
