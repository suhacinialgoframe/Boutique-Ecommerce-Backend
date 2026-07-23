from fastapi import APIRouter

from app.models.customer import Customer

from app.database.connection import database


router = APIRouter()


customers_collection = database["customers"]


# Create Customer
@router.post("/customers")
def create_customer(customer: Customer):

    # Check duplicate email
    existing_customer = customers_collection.find_one(
        {
            "email": customer.email
        }
    )

    if existing_customer:
        return {
            "message": "Email already registered"
        }


    customer_data = customer.dict()

    result = customers_collection.insert_one(customer_data)

    return {
        "message": "Customer created successfully",
        "id": str(result.inserted_id)
    }


# Get All Customers
@router.get("/customers")
def get_customers():

    customers = []

    for customer in customers_collection.find():

        customer["_id"] = str(customer["_id"])
        customers.append(customer)

    return customers



# Get Customer By ID
@router.get("/customers/{id}")
def get_customer(id: str):

    from bson.objectid import ObjectId


    customer = customers_collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )


    if customer:

        customer["_id"] = str(customer["_id"])

        return customer


    return {
        "message": "Customer not found"
    }



# Update Customer
@router.put("/customers/{id}")
def update_customer(id: str, customer: Customer):

    from bson.objectid import ObjectId


    result = customers_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": customer.dict()
        }
    )


    if result.modified_count:

        return {
            "message": "Customer updated successfully"
        }


    return {
        "message": "Customer not found"
    }



# Delete Customer
@router.delete("/customers/{id}")
def delete_customer(id: str):

    from bson.objectid import ObjectId


    result = customers_collection.delete_one(
        {
            "_id": ObjectId(id)
        }
    )


    if result.deleted_count:

        return {
            "message": "Customer deleted successfully"
        }


    return {
        "message": "Customer not found"
    }