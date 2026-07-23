from fastapi import APIRouter
from app.database.connection import database


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


orders_collection = database["orders"]


# =====================================================
# TOTAL SALES REPORT
# =====================================================

@router.get("/total-sales")
def total_sales():

    pipeline = [

        {
            "$group": {
                "_id": None,
                "total_sales": {
                    "$sum": "$total_amount"
                }
            }
        }

    ]


    result = list(
        orders_collection.aggregate(pipeline)
    )


    if result:
        return {
            "total_sales": result[0]["total_sales"]
        }

    return {
        "total_sales": 0
    }



# =====================================================
# TOTAL ORDER COUNT REPORT
# =====================================================

@router.get("/order-count")
def order_count():

    total_orders = orders_collection.count_documents({})


    return {
        "total_orders": total_orders
    }