from fastapi import APIRouter

from app.database.connection import database

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

products_collection = database["products"]


# =====================================================
# SEARCH BY PRODUCT NAME
# =====================================================

@router.get("/product/{name}")
def search_product(name: str):

    products = list(

        products_collection.find(

            {
                "name": {
                    "$regex": name,
                    "$options": "i"
                }
            }

        )

    )

    for product in products:

        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

    return products


# =====================================================
# SEARCH BY PRICE RANGE
# =====================================================

@router.get("/price")
def search_by_price(min_price: float, max_price: float):

    products = list(

        products_collection.find(

            {
                "price": {
                    "$gte": min_price,
                    "$lte": max_price
                }
            }

        )

    )

    for product in products:

        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

    return products