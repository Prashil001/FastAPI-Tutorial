import sqlite3
from fastapi import FastAPI

conn = sqlite3.connect("test.db",check_same_thread=False)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT
    )
""")

conn.commit()

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"successfully created table."
    }