from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    product_id: str
    quantity: int


class Cart(BaseModel):
    customer_id: str
    items: List[CartItem]