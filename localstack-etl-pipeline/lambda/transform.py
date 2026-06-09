import boto3
import csv

s3 = boto3.client(
    "s3",
    endpoint_url="http://host.docker.internal:4566",
    aws_access_key_id="admin",
    aws_secret_access_key="admin",
    region_name="ap-south-1"
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:4566",
    aws_access_key_id="admin",
    aws_secret_access_key="admin",
    region_name="ap-south-1"
)

table = dynamodb.Table("sales_summary")


def lambda_handler(event, context):

    for record in event["Records"]:

        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        response = s3.get_object(Bucket=bucket, Key=key)

        rows = response["Body"].read().decode().splitlines()

        reader = csv.DictReader(rows)

        for row in reader:

            total_amount = (
                int(row["quantity"]) *
                int(row["price"])
            )

            table.put_item(
                Item={
                    "order_id": row["order_id"],
                    "product": row["product"],
                    "quantity": int(row["quantity"]),
                    "price": int(row["price"]),
                    "total_amount": total_amount
                }
            )

    return {
        "statusCode": 200
    }