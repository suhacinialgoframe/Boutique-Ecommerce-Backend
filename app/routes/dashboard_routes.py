from fastapi import APIRouter
from app.database.connection import database


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


orders_collection = database["orders"]
users_collection = database["users"]
products_collection = database["products"]


# =====================================================
# CUSTOMER WISE TOTAL SPENDING
# =====================================================

@router.get("/customer-sales")
def customer_sales():

    pipeline = [

        {
            "$group": {
                "_id": "$customer_id",
                "total_spent": {
                    "$sum": "$total_amount"
                }
            }
        },

        {
            "$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "_id",
                "as": "customer"
            }
        },

        {
            "$unwind": "$customer"
        },

        {
            "$project": {
                "_id": 0,
                "customer_name": "$customer.name",
                "email": "$customer.email",
                "total_spent": 1
            }
        }

    ]


    return list(
        orders_collection.aggregate(pipeline)
    )



# =====================================================
# ORDER STATUS SUMMARY
# =====================================================

@router.get("/order-status")
def order_status():

    pipeline = [

        {
            "$group": {
                "_id": "$status",
                "count": {
                    "$sum": 1
                }
            }
        },

        {
            "$project": {
                "_id": 0,
                "status": "$_id",
                "count": 1
            }
        }

    ]


    return list(
        orders_collection.aggregate(pipeline)
    )



# =====================================================
# PRODUCT SALES COUNT
# =====================================================

@router.get("/product-sales")
def product_sales():

    pipeline = [

        {
            "$unwind": "$items"
        },

        {
            "$group": {
                "_id": "$items.product_id",
                "total_quantity_sold": {
                    "$sum": "$items.quantity"
                }
            }
        },

        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
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
                "product_name": "$product.name",
                "total_quantity_sold": 1
            }
        }

    ]


    return list(
        orders_collection.aggregate(pipeline)
    )