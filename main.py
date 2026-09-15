from fastapi import FastAPI

# -------------------------------------------------------
# Path Parameters
# -------------------------------------------------------
# Path parameters are dynamic values passed inside the URL.
#
# Example:
#   /about/Prashil
#   /product/101
#
# FastAPI automatically converts the value to the type
# specified in the function parameter.
# -------------------------------------------------------

app = FastAPI()


# =======================================================
# Example 1: Dynamic Route
# =======================================================

@app.get("/about/{name}")
def about(name: str):
    """
    GET /about/{name}

    Example:
    /about/Prashil
    """
    return {"message": f"Hello {name}. How are you?"}


# =======================================================
# Example 2: Integer Path Parameter
# =======================================================

@app.get("/product/{id}")
def get_product(id: int):
    """
    GET /product/{id}

    Example:
    /product/101
    """
    return {"product_id": id}