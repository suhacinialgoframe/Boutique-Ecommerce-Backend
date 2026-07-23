from fastapi import APIRouter
from app.database.connection import database


router = APIRouter()


users_collection = database["users"]


# =====================================================
# CUSTOMER + ORDERS + PRODUCTS LOOKUP
# =====================================================

@router.get("/lookup/customer-orders-products")
def customer_orders_products_lookup():

    pipeline = [

        # Join users with orders
        {
            "$lookup": {
                "from": "orders",
                "localField": "_id",
                "foreignField": "customer_id",
                "as": "orders"
            }
        },


        # Convert each order array item into document
        {
            "$unwind": {
                "path": "$orders",
                "preserveNullAndEmptyArrays": True
            }
        },


        # Join products using order items.product_id
        {
            "$lookup": {
                "from": "products",
                "localField": "orders.items.product_id",
                "foreignField": "_id",
                "as": "product_details"
            }
        },


        # Select required fields
        {
            "$project": {

                "_id": 0,

                "customer_name": "$name",

                "email": 1,

                "order_id": "$orders._id",

                "status": "$orders.status",

                "total_amount": "$orders.total_amount",

                "products": "$product_details.name"

            }
        }

    ]


    result = list(
        users_collection.aggregate(pipeline)
    )


    # Convert ObjectId to string
    for data in result:

        if data.get("order_id"):
            data["order_id"] = str(data["order_id"])


    return result