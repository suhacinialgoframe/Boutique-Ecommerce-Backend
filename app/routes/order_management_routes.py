from fastapi import APIRouter
from pydantic import BaseModel
from bson import ObjectId

from app.database.connection import database


router = APIRouter(
    prefix="/order-management",
    tags=["Order Management"]
)

orders_collection = database["orders"]


# =====================================================
# REQUEST MODEL
# =====================================================

class OrderStatus(BaseModel):
    status: str


# =====================================================
# ORDER DETAILS
# =====================================================

@router.get("/details")
def order_details():

    pipeline = [

        {
            "$lookup": {
                "from": "users",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer"
            }
        },

        {
            "$unwind": "$customer"
        },

        {
            "$unwind": "$items"
        },

        {
            "$lookup": {
                "from": "products",
                "localField": "items.product_id",
                "foreignField": "_id",
                "as": "product"
            }
        },

        {
            "$unwind": "$product"
        },

        {
            "$project": {

                "_id": 0,

                "order_id": {
                    "$toString": "$_id"
                },

                "customer_name": "$customer.name",

                "email": "$customer.email",

                "product_name": "$product.name",

                "quantity": "$items.quantity",

                "total_amount": 1,

                "status": 1
            }
        }

    ]

    return list(orders_collection.aggregate(pipeline))


# =====================================================
# UPDATE ORDER STATUS
# =====================================================

@router.put("/status/{order_id}")
def update_order_status(order_id: str, data: OrderStatus):

    result = orders_collection.update_one(

        {
            "_id": ObjectId(order_id)
        },

        {
            "$set": {
                "status": data.status
            }
        }

    )

    if result.modified_count == 1:

        return {
            "message": "Order status updated successfully"
        }

    return {
        "message": "Order not found or status already same"
    }


# =====================================================
# CANCEL ORDER
# =====================================================

@router.put("/cancel/{order_id}")
def cancel_order(order_id: str):

    result = orders_collection.update_one(

        {
            "_id": ObjectId(order_id)
        },

        {
            "$set": {
                "status": "Cancelled"
            }
        }

    )

    if result.modified_count == 1:

        return {
            "message": "Order cancelled successfully"
        }

    return {
        "message": "Order not found"
    }


# =====================================================
# TRACK ORDER
# =====================================================

@router.get("/track/{order_id}")
def track_order(order_id: str):

    order = orders_collection.find_one(
        {
            "_id": ObjectId(order_id)
        }
    )

    if not order:

        return {
            "message": "Order not found"
        }

    status = order["status"]

    messages = {

        "Placed": "Your order has been placed successfully.",

        "Confirmed": "Your order has been confirmed.",

        "Shipped": "Your order has been shipped.",

        "Delivered": "Your order has been delivered.",

        "Cancelled": "Your order has been cancelled."
    }

    return {

        "order_id": str(order["_id"]),

        "status": status,

        "message": messages.get(
            status,
            "Order status unavailable."
        )
    }