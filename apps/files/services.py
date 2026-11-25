from os import path
import uuid

from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.tenants.context import get_current_tenant
from .models import File
from .policies import get_policy, MIME_EXTENSIONS
from .s3 import get_s3


def _build_key(
    *,
    tenant_id,
    purpose: str,
    file_id: uuid.UUID,
    extension: str,
) -> str:
    now = timezone.now()
    upload_path = purpose.replace(".", "/")
    return f"tenants/{tenant_id}/{upload_path}/{now:%Y}/{now:%m}/{file_id}.{extension}"


def create_upload(
    *,
    user,
    purpose: str,
    filename: str,
    content_type: str,
    size: int,
) -> dict:
    policy = get_policy(purpose)

    if content_type not in policy.allowed_mime:
        raise ValidationError({"content-type": "This file type is not allowed."})

    if not 0 < size <= policy.max_size:
        raise ValidationError({"size": "This file size is not allowed."})

    tenant = get_current_tenant()
    file_id = uuid.uuid4()
    key = _build_key(
        tenant_id=tenant.pk,
        purpose=purpose,
        file_id=file_id,
        extension=MIME_EXTENSIONS[content_type],
    )

    file = File.objects.create(
        id=file_id,
        key=key,
        purpose=purpose,
        original_name=path.basename(filename)[:255],
        size=size,
    )

    upload = get_s3().generate_presigned_post(
        key=key,
        content_type=content_type,
        max_size=size,
    )
    return {"file_id": file.id, "upload": upload}


def get_download_url(
    file: File,
    *,
    as_attachment: bool = False,
) -> str:
    return get_s3().generate_presigned_get(
        key=file.key,
        download_name=file.original_name if as_attachment else None,
    )
