from src.app.local_config import *
from src.app.clients import get_s3_client

from src.app.services.s3_service import S3Service


s3 = get_s3_client()

service = S3Service(s3)

rows = service.get_csv_rows(
    bucket="raw-sales",
    key="sales.csv",
)

for row in rows:
    print(row)