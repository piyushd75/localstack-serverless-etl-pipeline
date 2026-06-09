from src.app.local_config import *
from src.app.clients import get_dynamodb_resource

from src.app.config import DYNAMODB_TABLE

from src.app.models.sales_record import SalesRecord

from src.app.services.dynamodb_service import (
    DynamoDBService,
)


dynamodb = get_dynamodb_resource()

table = dynamodb.Table(DYNAMODB_TABLE)

service = DynamoDBService(table)


record = SalesRecord(
    order_id="999",
    product="Test Product",
    quantity=1,
    price=100,
    total_amount=100,
)

service.save_sales_record(record)

print("Saved successfully.")