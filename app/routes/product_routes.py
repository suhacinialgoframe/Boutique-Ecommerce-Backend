from fastapi import APIRouter, Depends
from app.models.product import Product
from app.database.connection import database
from app.dependencies import verify_admin
from bson.objectid import ObjectId


router = APIRouter()

products_collection = database["products"]


# =====================================================
# CREATE PRODUCT (ADMIN ONLY)
# =====================================================

@router.post("/products")
def create_product(
    product: Product,
    user: dict = Depends(verify_admin)
):

    product_data = product.dict()

    result = products_collection.insert_one(product_data)

    return {
        "message": "Product created successfully",
        "id": str(result.inserted_id)
    }


# =====================================================
# GET ALL PRODUCTS
# =====================================================

@router.get("/products")
def get_products():

    products = []

    for product in products_collection.find():

        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

        products.append(product)

    return products



# =====================================================
# PRODUCT SEARCH + FILTER + SORT + PAGINATION
# =====================================================

@router.get("/products/search")
def search_products(
    name: str = None,
    category_id: str = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: str = None,
    page: int = 1,
    limit: int = 10
):

    query = {}


    if name:
        query["name"] = {
            "$regex": name,
            "$options": "i"
        }


    if category_id:
        query["category_id"] = category_id


    if min_price is not None or max_price is not None:

        query["price"] = {}

        if min_price is not None:
            query["price"]["$gte"] = min_price

        if max_price is not None:
            query["price"]["$lte"] = max_price


    skip = (page - 1) * limit


    products_cursor = products_collection.find(query)


    if sort_by:

        if sort_by == "price_asc":
            products_cursor = products_cursor.sort(
                "price",
                1
            )

        elif sort_by == "price_desc":
            products_cursor = products_cursor.sort(
                "price",
                -1
            )

        elif sort_by == "stock_asc":
            products_cursor = products_cursor.sort(
                "stock",
                1
            )

        elif sort_by == "stock_desc":
            products_cursor = products_cursor.sort(
                "stock",
                -1
            )


    products_cursor = products_cursor.skip(skip).limit(limit)


    products = []


    for product in products_cursor:

        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

        products.append(product)


    return {
        "page": page,
        "limit": limit,
        "count": len(products),
        "products": products
    }



# =====================================================
# GET PRODUCT BY ID
# =====================================================

@router.get("/products/{id}")
def get_product(id: str):

    product = products_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )


    if product:

        product["_id"] = str(product["_id"])

        if "category_id" in product:
            product["category_id"] = str(product["category_id"])

        return product


    return {
        "message": "Product not found"
    }



# =====================================================
# UPDATE PRODUCT (ADMIN ONLY)
# =====================================================

@router.put("/products/{id}")
def update_product(
    id: str,
    product: Product,
    user: dict = Depends(verify_admin)
):

    result = products_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": product.dict()
        }
    )


    if result.modified_count:

        return {
            "message": "Product updated successfully"
        }


    return {
        "message": "Product not found"
    }



# =====================================================
# DELETE PRODUCT (ADMIN ONLY)
# =====================================================

@router.delete("/products/{id}")
def delete_product(
    id: str,
    user: dict = Depends(verify_admin)
):

    result = products_collection.delete_one(
        {
            "_id": ObjectId(id)
        }
    )


    if result.deleted_count:

        return {
            "message": "Product deleted successfully"
        }


    return {
        "message": "Product not found"
    }