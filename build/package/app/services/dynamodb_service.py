class DynamoDBService:

    def __init__(self, table):
        self.table = table

    def save_sales_record(self, record):

        self.table.put_item(
            Item={
                "order_id": record.order_id,
                "product": record.product,
                "quantity": record.quantity,
                "price": record.price,
                "total_amount": record.total_amount,
            }
        )