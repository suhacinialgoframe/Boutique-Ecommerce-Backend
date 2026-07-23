from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.models.cart import Cart
from app.database.connection import database
from app.dependencies import verify_token


router = APIRouter()

cart_collection = database["cart"]


# Model for Add/Remove Cart operations
class CartItemRequest(BaseModel):
    customer_id: str
    product_id: str
    quantity: int


# ---------------- BASIC CART CRUD ----------------


# Create Cart
@router.post("/cart")
def create_cart(cart: Cart):

    cart_data = cart.dict()

    result = cart_collection.insert_one(cart_data)

    return {
        "message": "Cart created successfully",
        "id": str(result.inserted_id)
    }


# Get All Carts (Protected)
@router.get("/cart")
def get_cart(user_id: str = Depends(verify_token)):

    carts = []

    for cart in cart_collection.find():
        cart["_id"] = str(cart["_id"])
        carts.append(cart)

    return carts


# Get Cart By ID
@router.get("/cart/{id}")
def get_cart_by_id(id: str):

    from bson.objectid import ObjectId

    cart = cart_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )

    if cart:
        cart["_id"] = str(cart["_id"])
        return cart

    return {
        "message": "Cart not found"
    }



# ---------------- CART OPERATIONS ----------------


# Add Product To Cart (Protected)
@router.post("/cart/add")
def add_to_cart(
    item: CartItemRequest,
    user_id: str = Depends(verify_token)
):

    cart = cart_collection.find_one(
        {
            "customer_id": item.customer_id
        }
    )

    new_item = {
        "product_id": item.product_id,
        "quantity": item.quantity
    }


    if cart:

        cart_collection.update_one(
            {
                "customer_id": item.customer_id
            },
            {
                "$push": {
                    "items": new_item
                }
            }
        )

        return {
            "message": "Product added to cart"
        }


    else:

        cart_collection.insert_one(
            {
                "customer_id": item.customer_id,
                "items": [new_item]
            }
        )

        return {
            "message": "Cart created and product added"
        }



# Remove Product From Cart (Protected)
@router.delete("/cart/remove")
def remove_from_cart(
    customer_id: str,
    product_id: str,
    user_id: str = Depends(verify_token)
):

    result = cart_collection.update_one(
        {
            "customer_id": customer_id
        },
        {
            "$pull": {
                "items": {
                    "product_id": product_id
                }
            }
        }
    )


    if result.modified_count:

        return {
            "message": "Product removed from cart"
        }


    return {
        "message": "Product not found in cart"
    }



# Update Quantity (Protected)
# IMPORTANT: Keep this before /cart/{id}
@router.put("/cart/update-quantity")
def update_quantity(
    customer_id: str = Query(...),
    product_id: str = Query(...),
    quantity: int = Query(...),
    user_id: str = Depends(verify_token)
):

    result = cart_collection.update_one(
        {
            "customer_id": customer_id,
            "items.product_id": product_id
        },
        {
            "$set": {
                "items.$.quantity": quantity
            }
        }
    )


    if result.modified_count:

        return {
            "message": "Quantity updated successfully"
        }


    return {
        "message": "Product not found in cart"
    }



# Clear Cart (Protected)
@router.delete("/cart/clear")
def clear_cart(
    customer_id: str,
    user_id: str = Depends(verify_token)
):

    result = cart_collection.update_one(
        {
            "customer_id": customer_id
        },
        {
            "$set": {
                "items": []
            }
        }
    )


    if result.modified_count:

        return {
            "message": "Cart cleared successfully"
        }


    return {
        "message": "Cart not found"
    }



# Update Cart By ID
# Keep this at the bottom because /cart/{id} catches other paths
@router.put("/cart/{id}")
def update_cart(id: str, cart: Cart):

    from bson.objectid import ObjectId

    result = cart_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": cart.dict()
        }
    )

    if result.modified_count:

        return {
            "message": "Cart updated successfully"
        }


    return {
        "message": "Cart not found"
    }



# Delete Complete Cart
@router.delete("/cart/{id}")
def delete_cart(id: str):

    from bson.objectid import ObjectId

    result = cart_collection.delete_one(
        {
            "_id": ObjectId(id)
        }
    )

    if result.deleted_count:

        return {
            "message": "Cart deleted successfully"
        }


    return {
        "message": "Cart not found"
    }