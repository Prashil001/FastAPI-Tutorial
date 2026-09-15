import time

from fastapi import FastAPI, Request

# -------------------------------------------------------
# Middleware in FastAPI
# -------------------------------------------------------
# Middleware runs BEFORE and AFTER every request.
#
# Common uses:
# - Logging requests
# - Authentication
# - Measuring response time
# - Adding custom headers
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Custom Middleware
# =======================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Code before the request reaches the route
    start_time = time.time()

    print(f"Request: {request.method} {request.url}")

    # Pass request to the route
    response = await call_next(request)

    # Code after the route finishes
    process_time = time.time() - start_time

    print(f"Response Time: {process_time:.4f} seconds")

    # Add a custom header to every response
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    return response


# =======================================================
# Sample Routes
# =======================================================

@app.get("/")
def home():
    return {"message": "Home Page"}


@app.get("/about")
def about():
    return {"message": "About Page"}