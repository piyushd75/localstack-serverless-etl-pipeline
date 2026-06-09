from app.models.sales_record import SalesRecord


class TransformationService:

    @staticmethod
    def transform(row: dict) -> SalesRecord:

        quantity = int(row["quantity"])
        price = int(row["price"])

        return SalesRecord(
            order_id=row["order_id"],
            product=row["product"],
            quantity=quantity,
            price=price,
            total_amount=quantity * price,
        )