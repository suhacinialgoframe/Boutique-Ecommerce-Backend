from fastapi import APIRouter
from app.database.connection import database


router = APIRouter()


products_collection = database["products"]
users_collection = database["users"]


# =====================================================
# PRODUCT + CATEGORY LOOKUP
# =====================================================

@router.get("/lookup/products-category")
def products_category_lookup():

    pipeline = [

        {
            "$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category"
            }
        },

        {
            "$unwind": "$category"
        },

        {
            "$project": {
                "_id": 1,
                "name": 1,
                "price": 1,
                "stock": 1,
                "category.name": 1,
                "category.description": 1
            }
        }

    ]


    result = list(
        products_collection.aggregate(pipeline)
    )


    for product in result:
        product["_id"] = str(product["_id"])


    return result



# =====================================================
# CUSTOMER + ORDERS LOOKUP
# =====================================================

@router.get("/lookup/customer-orders")
def customer_orders_lookup():

    pipeline = [

        {
            "$lookup": {
                "from": "orders",
                "localField": "_id",
                "foreignField": "customer_id",
                "as": "orders"
            }
        },

        {
            "$project": {
                "_id": 0,
                "name": 1,
                "email": 1,
                "orders._id": 1,
                "orders.total_amount": 1,
                "orders.status": 1
            }
        }

    ]


    result = list(
        users_collection.aggregate(pipeline)
    )


    # Convert ObjectId into string
    for user in result:

        for order in user.get("orders", []):

            if "_id" in order:
                order["_id"] = str(order["_id"])


    return result