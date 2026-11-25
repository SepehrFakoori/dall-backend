from dataclasses import dataclass

from rest_framework.exceptions import ValidationError

MB = 1024 * 1024


MIME_EXTENSIONS = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "application/pdf": "pdf",
}


@dataclass(frozen=True)
class UploadPolicy:
    purpose: str
    allowed_mime: frozenset[str]
    max_size: int

    def __post_init__(self):
        unknown = self.allowed_mime.difference(MIME_EXTENSIONS)
        if unknown:
            raise ValueError(f"No extension defined for: {sorted(unknown)}")


_registry: dict[str, UploadPolicy] = {}


def register(policy: UploadPolicy) -> None:
    _registry[policy.purpose] = policy


def get_policy(purpose: str) -> UploadPolicy:
    try:
        return _registry[purpose]
    except KeyError:
        raise ValidationError("Unknown upload purpose")
