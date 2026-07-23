from fastapi import APIRouter, Depends
from app.models.payment import Payment
from app.database.connection import database
from app.dependencies import verify_token
from bson.objectid import ObjectId


router = APIRouter()

payments_collection = database["payments"]


# Create Payment (Protected)
@router.post("/payments")
def create_payment(
    payment: Payment,
    user_id: str = Depends(verify_token)
):

    payment_data = payment.dict()

    result = payments_collection.insert_one(payment_data)

    return {
        "message": "Payment created successfully",
        "id": str(result.inserted_id)
    }



# Get All Payments (Protected)
@router.get("/payments")
def get_payments(
    user_id: str = Depends(verify_token)
):

    payments = []

    for payment in payments_collection.find():

        payment["_id"] = str(payment["_id"])
        payments.append(payment)

    return payments



# Get Payment By ID
@router.get("/payments/{id}")
def get_payment(id: str):

    payment = payments_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )

    if payment:

        payment["_id"] = str(payment["_id"])
        return payment

    return {
        "message": "Payment not found"
    }



# Update Payment Status (Protected)
@router.put("/payments/status/{id}")
def update_payment_status(
    id: str,
    payment_status: str,
    user_id: str = Depends(verify_token)
):

    payment = payments_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )


    if not payment:

        return {
            "message": "Payment not found"
        }


    result = payments_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": {
                "payment_status": payment_status
            }
        }
    )


    # Confirm order after successful payment
    if payment_status.lower() == "success":

        orders_collection = database["orders"]

        orders_collection.update_one(
            {
                "_id": ObjectId(payment["order_id"])
            },
            {
                "$set": {
                    "status": "Confirmed"
                }
            }
        )


    if result.matched_count:

        return {
            "message": "Payment processed successfully"
        }


    return {
        "message": "Payment not found"
    }



# Delete Payment (Protected)
@router.delete("/payments/{id}")
def delete_payment(
    id: str,
    user_id: str = Depends(verify_token)
):

    result = payments_collection.delete_one(
        {
            "_id": ObjectId(id)
        }
    )


    if result.deleted_count:

        return {
            "message": "Payment deleted successfully"
        }


    return {
        "message": "Payment not found"
    }