import csv


class S3Service:

    def __init__(self, s3_client):
        self.s3_client = s3_client

    def get_csv_rows(self, bucket, key):

        response = self.s3_client.get_object(
            Bucket=bucket,
            Key=key,
        )

        rows = (
            response["Body"]
            .read()
            .decode("utf-8")
            .splitlines()
        )

        return csv.DictReader(rows)