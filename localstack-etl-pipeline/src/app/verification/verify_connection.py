from src.app.local_config import *
from src.app.clients import get_s3_client

from src.app.config import (
    S3_BUCKET,
    LOCALSTACK_ENDPOINT,
)


print(
    f"Endpoint: {LOCALSTACK_ENDPOINT}"
)

print(
    f"Bucket from env: {S3_BUCKET}"
)


s3 = get_s3_client()

response = s3.list_buckets()

print(response["Buckets"])