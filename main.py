from fastapi import FastAPI, Depends, HTTPException

# -------------------------------------------------------
# Dependency Injection in FastAPI
# -------------------------------------------------------
# A dependency is a function that FastAPI executes before
# your route function.
#
# It helps reuse common logic like:
# - Authentication
# - Database connections
# - Validation
# - Logging
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Basic Dependency
# =======================================================

def welcome_message():
    return "Welcome to FastAPI Dependency Injection"


@app.get("/")
def home(message: str = Depends(welcome_message)):
    return {"message": message}


# =======================================================
# Dependency with Query Parameter
# =======================================================

def get_username(name: str = "Guest"):
    return name


@app.get("/profile")
def profile(username: str = Depends(get_username)):
    return {
        "message": f"Hello {username}"
    }


# =======================================================
# Reusable Authentication Dependency
# =======================================================

def verify_api_key(api_key: str):
    if api_key != "fastapi123":
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return api_key


@app.get("/dashboard")
def dashboard(api_key: str = Depends(verify_api_key)):
    return {
        "message": "Welcome to Dashboard"
    }


@app.get("/settings")
def settings(api_key: str = Depends(verify_api_key)):
    return {
        "message": "Settings Page"
    }