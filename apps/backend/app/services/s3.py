import uuid

import aioboto3
from botocore.config import Config

from app.config import settings

_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
_EXT_MAP = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif"}


def _session() -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
    )


async def upload_avatar(data: bytes, content_type: str, user_id: str) -> str:
    if content_type not in _ALLOWED_TYPES:
        raise ValueError(f"Недопустимый тип файла: {content_type}")
    if len(data) > _MAX_BYTES:
        raise ValueError("Файл слишком большой (максимум 5 МБ)")

    ext = _EXT_MAP[content_type]
    key = f"public/avatars/{user_id}-{uuid.uuid4().hex[:8]}.{ext}"

    async with _session().client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        config=Config(s3={"addressing_style": settings.s3_addressing_style}),
    ) as s3:
        await s3.put_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
            Body=data,
            ContentType=content_type,
        )

    return f"{settings.s3_public_url}/{settings.s3_bucket_name}/{key}"
