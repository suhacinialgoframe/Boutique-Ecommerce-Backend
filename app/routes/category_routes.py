from fastapi import APIRouter
from app.models.category import Category
from app.database.connection import database
from bson.objectid import ObjectId


router = APIRouter()

categories_collection = database["categories"]


# Create Category
@router.post("/categories")
def create_category(category: Category):

    # Check duplicate category
    existing_category = categories_collection.find_one(
        {
            "name": category.name
        }
    )

    if existing_category:
        return {
            "message": "Category already exists"
        }

    category_data = category.dict()

    result = categories_collection.insert_one(category_data)

    return {
        "message": "Category created successfully",
        "id": str(result.inserted_id)
    }


# Get All Categories
@router.get("/categories")
def get_categories():

    categories = []

    for category in categories_collection.find():
        category["_id"] = str(category["_id"])
        categories.append(category)

    return categories


# Get Category By ID
@router.get("/categories/{id}")
def get_category(id: str):

    category = categories_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )

    if category:
        category["_id"] = str(category["_id"])
        return category

    return {
        "message": "Category not found"
    }


# Update Category
@router.put("/categories/{id}")
def update_category(id: str, category: Category):

    result = categories_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": category.dict()
        }
    )

    if result.modified_count:
        return {
            "message": "Category updated successfully"
        }

    return {
        "message": "Category not found"
    }


# Delete Category
@router.delete("/categories/{id}")
def delete_category(id: str):

    result = categories_collection.delete_one(
        {
            "_id": ObjectId(id)
        }
    )

    if result.deleted_count:
        return {
            "message": "Category deleted successfully"
        }

    return {
        "message": "Category not found"
    }