from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


# =======================================================
# Pydantic Models
# =======================================================

class Address(BaseModel):
    city: str
    country: str


class User(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    age: Annotated[int, Field(gt=0, lt=120)]
    email: EmailStr
    is_student: bool = False          # Default value
    phone: str | None = None          # Optional field
    address: Address                  # Nested model


# =======================================================
# Create User
# =======================================================

@app.post("/users")
def create_user(user: User):
    """
    Request body is automatically validated
    using the User Pydantic model.
    """
    return {
        "message": "User created successfully",
        "data": user
    }



# =======================================================
# Multiple Body Parameters
# =======================================================

class Product(BaseModel):
    name: str
    price: float


@app.post("/order")
def create_order(
    user: User,
    product: Product,
    quantity: Annotated[int, Body(gt=0)]
):
    return {
        "user": user.name,
        "product": product.name,
        "quantity": quantity
    }