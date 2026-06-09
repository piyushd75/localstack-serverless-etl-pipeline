from dataclasses import dataclass


@dataclass
class SalesRecord:
    order_id: str
    product: str
    quantity: int
    price: int
    total_amount: int