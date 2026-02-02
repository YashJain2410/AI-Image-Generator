import boto3
import uuid

from app.core.config import settings

class S3Client:
    def __init__(self):
        if not settings.AWS_S3_BUCKET:
            raise RuntimeError("S3 bucket not configured")
        
        self.bucket = settings.AWS_S3_BUCKET
        self.client = boto3.client(
            "s3",
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            region_name = settings.AWS_REGION,
        )
    
    def upload_file(self, file_bytes: bytes, content_type: str) -> str:
        import uuid

        key = f"uploads/{uuid.uuid4().hex}"

        self.client.put_object(
            Bucket = self.bucket,
            Key = key,
            Body = file_bytes,
            ContentType = content_type,
        )

        return f"https://{self.bucket}.s3.amazon.com/{key}"