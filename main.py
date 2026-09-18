import sqlite3
from fastapi import FastAPI

# -------------------------------------------------------
# SQLite Database Setup
# -------------------------------------------------------
# sqlite3 is Python's built-in database library.
# It creates a local database file that doesn't require
# a separate database server.
# -------------------------------------------------------

# Create or connect to the database
# "test.db" will be created automatically if it doesn't exist.
conn = sqlite3.connect("test.db", check_same_thread=False)

# Create a cursor object
# A cursor is used to execute SQL queries.
cur = conn.cursor()


# =======================================================
# Create Table
# =======================================================
# IF NOT EXISTS prevents the table from being created again
# every time the server restarts.

cur.execute("""
CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT
)
""")

# Save changes to the database
conn.commit()


# =======================================================
# FastAPI App
# =======================================================

app = FastAPI()


# =======================================================
# Home Route
# =======================================================

@app.get("/")
def home():
    return {
        "message": "Database connected and todos table is ready."
    }