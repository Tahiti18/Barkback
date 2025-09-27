import boto3, time
from app.config import settings

s3 = boto3.client(
    "s3",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id or None,
    aws_secret_access_key=settings.aws_secret_access_key or None,
)

def presign_put(key: str, content_type: str, expires: int = 900):
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.aws_s3_bucket, "Key": key, "ContentType": content_type},
        ExpiresIn=expires,
    )

def presign_get(key: str, expires: int = 900):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.aws_s3_bucket, "Key": key},
        ExpiresIn=expires,
    )
