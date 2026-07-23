from fastapi import APIRouter, Depends
from app.models.order import Order
from app.database.connection import database
from app.dependencies import verify_token
from bson.objectid import ObjectId


router = APIRouter()

orders_collection = database["orders"]
products_collection = database["products"]


# Create Order (Protected + Stock Update)
@router.post("/orders")
def create_order(
    order: Order,
    user_id: str = Depends(verify_token)
):

    order_data = order.dict()


    # Reduce product stock
    for item in order.items:

        product = products_collection.find_one(
            {
                "_id": ObjectId(item.product_id)
            }
        )


        if not product:
            return {
                "message": "Product not found"
            }


        if product["stock"] < item.quantity:
            return {
                "message": "Not enough stock available"
            }


        products_collection.update_one(
            {
                "_id": ObjectId(item.product_id)
            },
            {
                "$inc": {
                    "stock": -item.quantity
                }
            }
        )


    result = orders_collection.insert_one(order_data)


    return {
        "message": "Order created successfully",
        "id": str(result.inserted_id)
    }



# Get All Orders (Protected)
@router.get("/orders")
def get_orders(
    user_id: str = Depends(verify_token)
):

    orders = []

    for order in orders_collection.find():

        order["_id"] = str(order["_id"])
        orders.append(order)

    return orders



# Get Order By ID
@router.get("/orders/{id}")
def get_order(id: str):

    order = orders_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )


    if order:

        order["_id"] = str(order["_id"])
        return order


    return {
        "message": "Order not found"
    }



# Update Order
@router.put("/orders/{id}")
def update_order(
    id: str,
    order: Order
):

    result = orders_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": order.dict()
        }
    )


    if result.modified_count:

        return {
            "message": "Order updated successfully"
        }


    return {
        "message": "Order not found"
    }



# Delete Order
@router.delete("/orders/{id}")
def delete_order(id: str):

    result = orders_collection.delete_one(
        {
            "_id": ObjectId(id)
        }
    )


    if result.deleted_count:

        return {
            "message": "Order deleted successfully"
        }


    return {
        "message": "Order not found"
    }



# Get Orders By Customer (Order History)
@router.get("/orders/customer/{customer_id}")
def get_orders_by_customer(
    customer_id: str,
    user_id: str = Depends(verify_token)
):

    orders = []

    for order in orders_collection.find(
        {
            "customer_id": customer_id
        }
    ):

        order["_id"] = str(order["_id"])
        orders.append(order)


    return orders



# Update Order Status
@router.put("/orders/status/{id}")
def update_order_status(
    id: str,
    status: str,
    user_id: str = Depends(verify_token)
):

    result = orders_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": {
                "status": status
            }
        }
    )


    if result.modified_count:

        return {
            "message": "Order status updated successfully"
        }


    return {
        "message": "Order not found"
    }



# Cancel Order
@router.put("/orders/cancel/{id}")
def cancel_order(
    id: str,
    user_id: str = Depends(verify_token)
):

    result = orders_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": {
                "status": "Cancelled"
            }
        }
    )


    if result.modified_count:

        return {
            "message": "Order cancelled successfully"
        }


    return {
        "message": "Order not found"
    }