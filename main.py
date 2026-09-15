from fastapi import FastAPI
from pydantic import BaseModel

# -------------------------------------------------------
# Response Model in FastAPI
# -------------------------------------------------------
# A response_model controls what data is sent back
# to the client.
#
# Even if the function returns extra fields
# (like passwords), FastAPI removes them automatically.
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Request Model
# =======================================================
# This model defines the data that the client sends.

class User(BaseModel):
    name: str
    age: int
    password: str


# =======================================================
# Response Model
# =======================================================
# This model defines what the client receives.
# Notice that "password" is intentionally omitted.

class UserResponse(BaseModel):
    name: str
    age: int


# =======================================================
# Create User Endpoint
# =======================================================
# Request Body  -> User
# Response Body -> UserResponse

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    """
    Example Request:

    {
        "name": "Prashil",
        "age": 21,
        "password": "secret123"
    }

    Response:

    {
        "name": "Prashil",
        "age": 21
    }
    """

    # Returning the entire user object.
    # FastAPI automatically removes the password
    # because of response_model=UserResponse.

    return user