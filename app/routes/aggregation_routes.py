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


    for item in result:

        if "_id" in item:
            item["_id"] = str(item["_id"])


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

        product = result[0]


        # Convert MongoDB ObjectId
        if "_id" in product:
            product["_id"] = str(product["_id"])


        if "category_id" in product:
            product["category_id"] = str(product["category_id"])


        return product



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

        if "_id" in product:
            product["_id"] = str(product["_id"])


    return result