from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# -------------------------------------------------------
# Exception Handling in FastAPI
# -------------------------------------------------------
# This example demonstrates:
# - HTTPException
# - Custom Exception
# - Global HTTP Exception Handler
# - Global Custom Exception Handler
# - Global Exception Handler (Unexpected Errors)
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Custom Exception
# =======================================================

class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id


# Fake Database
users = {
    1: "Prashil",
    2: "Rahul"
}


# =======================================================
# Route 1 - HTTPException
# =======================================================

@app.get("/http-user/{user_id}")
def get_http_user(user_id: int):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"user": users[user_id]}


# =======================================================
# Route 2 - Custom Exception
# =======================================================

@app.get("/custom-user/{user_id}")
def get_custom_user(user_id: int):

    if user_id not in users:
        raise UserNotFoundException(user_id)

    return {"user": users[user_id]}


# =======================================================
# Route 3 - Unexpected Error
# =======================================================

@app.get("/divide")
def divide():

    # This intentionally raises ZeroDivisionError
    result = 10 / 0

    return {"result": result}


# =======================================================
# Global HTTP Exception Handler
# =======================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


# =======================================================
# Global Custom Exception Handler
# =======================================================

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": f"User with ID {exc.user_id} does not exist."
        }
    )


# =======================================================
# Global Exception Handler
# =======================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Something went wrong."
        }
    )