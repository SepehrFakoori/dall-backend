from apps.files.policies import UploadPolicy, MB

AVATAR_PURPOSE = "users.avatar"


UPLOAD_POLICIES = (
    UploadPolicy(
        purpose=AVATAR_PURPOSE,
        allowed_mime=frozenset({"image/jpeg", "image/png", "image/webp"}),
        max_size=5 * MB,
    ),
)
