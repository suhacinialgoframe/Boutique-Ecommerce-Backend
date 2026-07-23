from pydantic import BaseModel


class Payment(BaseModel):
    order_id: str
    customer_id: str
    amount: float
    payment_method: str
    payment_status: str
    transaction_id: str