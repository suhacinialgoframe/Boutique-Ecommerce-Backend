from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    name: str
    description: str
    price: float
    category_id: str
    sizes: List[str]
    colors: List[str]
    stock: int