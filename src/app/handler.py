from app.clients import (
    get_dynamodb_resource,
    get_s3_client,
)

from app.config import DYNAMODB_TABLE

from app.services.dynamodb_service import (
    DynamoDBService,
)

from app.services.s3_service import (
    S3Service,
)

from app.services.transformation_service import (
    TransformationService,
)


s3_client = get_s3_client()

dynamodb = get_dynamodb_resource()

table = dynamodb.Table(DYNAMODB_TABLE)


s3_service = S3Service(s3_client)

dynamodb_service = DynamoDBService(table)


def lambda_handler(event, context):

    print(
        f"Received event: {event}"
    )

    for record in event["Records"]:

        bucket = (
            record["s3"]["bucket"]["name"]
        )

        key = (
            record["s3"]["object"]["key"]
        )

        rows = (
            s3_service.get_csv_rows(
                bucket,
                key,
            )
        )

        for row in rows:

            sales_record = (
                TransformationService.transform(
                    row
                )
            )

            dynamodb_service.save_sales_record(
                sales_record
            )

    return {
        "statusCode": 200,
        "body": "Processing completed",
    }