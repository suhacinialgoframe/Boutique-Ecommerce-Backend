from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    status: str