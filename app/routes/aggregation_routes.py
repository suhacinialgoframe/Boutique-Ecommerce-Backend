from fastapi import APIRouter
from app.database.connection import database

router = APIRouter()

products_collection = database["products"]


# =====================================================
# TOTAL PRODUCTS PER CATEGORY
# =====================================================

@router.get("/aggregation/products-by-category")
def products_by_category():

    pipeline = [
        {
            "$group": {
                "_id": "$category_id",
                "total_products": {
                    "$sum": 1
                }
            }
        }
    ]

    result = list(products_collection.aggregate(pipeline))

    return result


# =====================================================
# AVERAGE PRODUCT PRICE
# =====================================================

@router.get("/aggregation/average-price")
def average_product_price():

    pipeline = [
        {
            "$group": {
                "_id": None,
                "average_price": {
                    "$avg": "$price"
                }
            }
        }
    ]

    result = list(products_collection.aggregate(pipeline))

    if result:
        return {
            "average_price": result[0]["average_price"]
        }

    return {
        "average_price": 0
    }


# =====================================================
# MAXIMUM PRICE PRODUCT
# =====================================================

@router.get("/aggregation/max-price")
def maximum_price_product():

    pipeline = [
        {
            "$sort": {
                "price": -1
            }
        },
        {
            "$limit": 1
        }
    ]

    result = list(products_collection.aggregate(pipeline))

    if result:

        result[0]["_id"] = str(result[0]["_id"])

        return result[0]

    return {
        "message": "No products found"
    }


# =====================================================
# INVENTORY VALUE
# =====================================================

@router.get("/aggregation/inventory-value")
def inventory_value():

    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "price": 1,
                "stock": 1,
                "inventory_value": {
                    "$multiply": [
                        "$price",
                        "$stock"
                    ]
                }
            }
        }
    ]

    result = list(products_collection.aggregate(pipeline))

    for product in result:
        product["_id"] = str(product["_id"])

    return result