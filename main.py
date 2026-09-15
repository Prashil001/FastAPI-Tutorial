from typing import Annotated
from fastapi import FastAPI, Query

# -------------------------------------------------------
# Query Parameters
# -------------------------------------------------------
# Query parameters are values passed after the '?' in a URL.
#
# Example:
# /search?item=laptop&page=2
#
# They are commonly used for:
# - Searching
# - Filtering
# - Pagination
# - Sorting
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Example 1: Required Query Parameter
# =======================================================

@app.get("/search")
def search(item: str):
    """
    Example:
    /search?item=laptop
    """
    return {"search_item": item}


# =======================================================
# Example 2: Optional Query Parameter
# =======================================================

@app.get("/profile")
def profile(name: str | None = None):
    """
    Example:
    /profile
    /profile?name=Prashil
    """
    return {"name": name}


# =======================================================
# Example 3: Default Value
# =======================================================

@app.get("/products")
def products(page: int = 1):
    """
    Example:
    /products
    /products?page=3
    """
    return {"current_page": page}


# =======================================================
# Example 4: Multiple Query Parameters
# =======================================================

@app.get("/items")
def items(category: str, page: int = 1, limit: int = 10):
    """
    Example:
    /items?category=electronics&page=2&limit=20
    """
    return {
        "category": category,
        "page": page,
        "limit": limit
    }


# =======================================================
# Example 5: Boolean Query Parameter
# =======================================================

@app.get("/users")
def users(active: bool = True):
    """
    Example:
    /users
    /users?active=false
    """
    return {"active_users": active}


# =======================================================
# Example 6: Validation using Query()
# =======================================================

@app.get("/books")
def books(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    """
    Example:
    /books?page=2&limit=20
    """
    return {
        "page": page,
        "limit": limit
    }


# =======================================================
# Example 7: String Validation
# =======================================================

@app.get("/login")
def login(
    username: Annotated[str, Query(min_length=3, max_length=20)],
):
    """
    Example:
    /login?username=prashil
    """
    return {"username": username}