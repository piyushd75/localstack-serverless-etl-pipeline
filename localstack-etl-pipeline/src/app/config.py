import os


AWS_ACCESS_KEY_ID = os.getenv(
    "AWS_ACCESS_KEY_ID"
)

AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY"
)

AWS_DEFAULT_REGION = os.getenv(
    "AWS_DEFAULT_REGION",
    "ap-south-1",
)

LOCALSTACK_ENDPOINT = os.getenv(
    "LOCALSTACK_ENDPOINT"
)

S3_BUCKET = os.getenv(
    "S3_BUCKET"
)

DYNAMODB_TABLE = os.getenv(
    "DYNAMODB_TABLE"
)