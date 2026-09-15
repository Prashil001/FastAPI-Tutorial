from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# -------------------------------------------------------
# HTTP Status Codes & Error Handling
# -------------------------------------------------------
# This example demonstrates:
# - Returning custom status codes
# - Using HTTPException
# - Basic error handling
# - Custom success responses
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Pydantic Model
# =======================================================

class User(BaseModel):
    name: str
    age: int


# Fake Database
users = []


# =======================================================
# CREATE USER
# =======================================================

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    """
    Creates a new user.

    Success Status Code:
    201 Created
    """

    users.append(user)
    return {
        "message": "User created successfully",
        "data": user
    }


# =======================================================
# GET USER
# =======================================================

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Returns a user by ID.

    Error:
    404 Not Found
    """

    if user_id < 1 or user_id > len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "message": "User found",
        "data": users[user_id - 1]
    }


# =======================================================
# DELETE USER
# =======================================================

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Deletes a user.

    Success:
    200 OK

    Error:
    404 Not Found
    """

    if user_id < 1 or user_id > len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    deleted_user = users.pop(user_id - 1)

    return {
        "message": "User deleted successfully",
        "data": deleted_user
    }


# =======================================================
# AGE VALIDATION
# =======================================================

@app.post("/check-age")
def check_age(user: User):
    """
    Demonstrates custom validation.

    Error:
    400 Bad Request
    """

    if user.age < 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be at least 18 years old"
        )

    return {
        "message": "Age verification successful"
    }