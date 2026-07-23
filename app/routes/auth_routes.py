from fastapi import APIRouter, Depends

from app.models.user import User
from app.models.auth import LoginRequest

from app.database.connection import database

from app.security import create_access_token

from app.dependencies import verify_token


router = APIRouter()


users_collection = database["users"]


# Register User
@router.post("/register")
def register_user(user: User):

    # Check if email already exists
    existing_user = users_collection.find_one(
        {
            "email": user.email
        }
    )

    if existing_user:
        return {
            "message": "Email already registered"
        }

    user_data = user.dict()

    result = users_collection.insert_one(user_data)

    return {
        "message": "User registered successfully",
        "id": str(result.inserted_id)
    }


# Get All Users (Protected)
@router.get("/users")
def get_users(user_id: str = Depends(verify_token)):

    users = []

    for user in users_collection.find():

        user["_id"] = str(user["_id"])
        users.append(user)

    return users


# Login User
@router.post("/login")
def login_user(login_data: LoginRequest):

    user = users_collection.find_one(
        {
            "email": login_data.email
        }
    )

    if not user:
        return {
            "message": "User not found"
        }


    if user["password"] != login_data.password:

        return {
            "message": "Invalid password"
        }


    token = create_access_token(
        {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "role": user.get("role", "customer")
        }
    )


    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }