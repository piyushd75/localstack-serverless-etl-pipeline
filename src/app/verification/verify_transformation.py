from src.app.local_config import *
from src.app.services.transformation_service import (
    TransformationService,
)

row = {
    "order_id": "1",
    "product": "Laptop",
    "quantity": "2",
    "price": "60000",
}

record = TransformationService.transform(row)

print(record)
print(record.total_amount)