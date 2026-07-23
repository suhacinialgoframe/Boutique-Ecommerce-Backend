from fastapi import APIRouter
from app.database.connection import database

router = APIRouter(
    prefix="/pagination",
    tags=["Pagination & Sorting"]
)

products_collection = database["products"]


# =====================================================
# PAGINATION
# =====================================================

@router.get("/products")
def get_products_page(page: int = 1, limit: int = 5):

    skip = (page - 1) * limit

    products = list(
        products_collection.find().skip(skip).limit(limit)
    )

    for product in products:
        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

    return products


# =====================================================
# SORT BY PRICE
# =====================================================

@router.get("/sort/price")
def sort_by_price():

    products = list(
        products_collection.find().sort("price", 1)
    )

    for product in products:
        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

    return products


# =====================================================
# SORT BY STOCK
# =====================================================

@router.get("/sort/stock")
def sort_by_stock():

    products = list(
        products_collection.find().sort("stock", -1)
    )

    for product in products:
        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

    return products


# =====================================================
# SORT BY NAME
# =====================================================

@router.get("/sort/name")
def sort_by_name():

    products = list(
        products_collection.find().sort("name", 1)
    )

    for product in products:
        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

    return products