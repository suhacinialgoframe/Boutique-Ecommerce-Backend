from fastapi import APIRouter

from app.database.connection import database

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)

users_collection = database["users"]
products_collection = database["products"]
categories_collection = database["categories"]
orders_collection = database["orders"]


# =====================================================
# PROJECT STATISTICS
# =====================================================

@router.get("/")
def project_statistics():

    total_users = users_collection.count_documents({})

    total_products = products_collection.count_documents({})

    total_categories = categories_collection.count_documents({})

    total_orders = orders_collection.count_documents({})

    revenue = list(

        orders_collection.aggregate([

            {
                "$group": {
                    "_id": None,
                    "total_revenue": {
                        "$sum": "$total_amount"
                    }
                }
            }

        ])

    )

    total_revenue = 0

    if revenue:

        total_revenue = revenue[0]["total_revenue"]

    return {

        "total_users": total_users,

        "total_products": total_products,

        "total_categories": total_categories,

        "total_orders": total_orders,

        "total_revenue": total_revenue
    }