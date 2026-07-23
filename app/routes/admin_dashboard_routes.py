from fastapi import APIRouter
from app.database.connection import database


router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)


products_collection = database["products"]
orders_collection = database["orders"]


# =====================================================
# INVENTORY STATUS
# =====================================================

@router.get("/inventory")
def inventory_status():

    pipeline = [

        {
            "$project": {
                "_id": 0,
                "product_name": "$name",
                "stock": 1,
                "availability": {
                    "$cond": [
                        {
                            "$gt": [
                                "$stock",
                                0
                            ]
                        },
                        "In Stock",
                        "Out of Stock"
                    ]
                }
            }
        }

    ]


    return list(
        products_collection.aggregate(pipeline)
    )



# =====================================================
# LOW STOCK ALERT
# =====================================================

@router.get("/low-stock")
def low_stock():

    pipeline = [

        {
            "$match": {
                "stock": {
                    "$lt": 10
                }
            }
        },

        {
            "$project": {
                "_id": 0,
                "product_name": "$name",
                "stock": 1
            }
        }

    ]


    return list(
        products_collection.aggregate(pipeline)
    )



# =====================================================
# REVENUE SUMMARY
# =====================================================

@router.get("/revenue-summary")
def revenue_summary():

    pipeline = [

        {
            "$group": {
                "_id": None,

                "total_revenue": {
                    "$sum": "$total_amount"
                },

                "total_orders": {
                    "$sum": 1
                },

                "average_order_value": {
                    "$avg": "$total_amount"
                }
            }
        },

        {
            "$project": {
                "_id": 0,
                "total_revenue": 1,
                "total_orders": 1,
                "average_order_value": 1
            }
        }

    ]


    result = list(
        orders_collection.aggregate(pipeline)
    )


    return result[0] if result else {}