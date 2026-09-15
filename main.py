from fastapi import FastAPI

# -------------------------------------------------------
# FastAPI Basics
# -------------------------------------------------------
# FastAPI is a modern Python web framework used for building
# APIs quickly. It is built on top of:
# - Starlette -> Handles web requests (routing, middleware).
# - Pydantic  -> Validates request and response data.
#
# Features:
# - Very fast performance (ASGI based)
# - Automatic Swagger & ReDoc documentation
# - Type hint based validation
# - Async support
# -------------------------------------------------------

# Create a FastAPI application instance.
app = FastAPI()


# =======================================================
# Route 1 : Home
# =======================================================

@app.get("/")
def home():
    """
    GET /
    Returns the home page message.
    """
    return {"message": "This is the home page."}


# =======================================================
# Route 2 : About
# =======================================================

@app.get("/about")
def about():
    """
    GET /about
    Returns the about page message.
    """
    return {"message": "This is the about page."}