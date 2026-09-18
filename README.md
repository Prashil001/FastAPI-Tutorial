# SQLAlchemy Basics with FastAPI

> Learn how to integrate **SQLAlchemy 2.0** with FastAPI using SQLite. This chapter covers database connections, models, sessions, CRUD operations, and dependency injection.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)

---

## 📚 What You'll Learn

- What is SQLAlchemy?
- What is an ORM?
- Connecting FastAPI with SQLite
- Creating Models
- Database Sessions
- CRUD Operations
- Dependency Injection with `Depends()`
- Common Interview Questions

---

# 📂 Project Structure

```text
11-sqlalchemy-basics/
│
├── app.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── test.db
├── requirements.txt
└── README.md
```

---

# What is SQLAlchemy?

**SQLAlchemy** is Python's most popular **ORM (Object Relational Mapper)**.

Instead of writing SQL manually, you interact with the database using Python classes.

### Without SQLAlchemy

```sql
INSERT INTO todos(title, description)
VALUES ('Learn SQLAlchemy', 'Practice ORM');
```

### With SQLAlchemy

```python
todo = Todo(
    title="Learn SQLAlchemy",
    description="Practice ORM"
)

db.add(todo)
db.commit()
```

---

# What is an ORM?

ORM stands for **Object Relational Mapper**.

It maps Python objects to database tables.

| Python | Database |
|---------|----------|
| Class | Table |
| Object | Row |
| Attribute | Column |

Example:

```python
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
```

Equivalent table:

| id | title |
|----|--------|
|1|Learn FastAPI|
|2|Study SQLAlchemy|

---

# Why Use SQLAlchemy?

| Without ORM | With ORM |
|-------------|----------|
| Write SQL manually | Write Python code |
| More repetitive | Cleaner |
| Harder to maintain | Easier |
| Less reusable | More reusable |

---

# Architecture

```text
Client
   │
   ▼
FastAPI
   │
Depends(get_db)
   │
CRUD Functions
   │
   ▼
SQLAlchemy
   │
Engine → Session
   │
   ▼
SQLite (test.db)
```

---

# Step 1: Create the Database Engine

`database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

### What is `create_engine()`?

`create_engine()` creates the connection between FastAPI and SQLite.

```text
FastAPI
   │
Engine
   │
SQLite
```

---

# Step 2: Database Session

```python
SessionLocal = sessionmaker(...)
```

A **Session** represents one conversation with the database.

| Request | Session |
|---------|---------|
| Request 1 | Session A |
| Request 2 | Session B |
| Request 3 | Session C |

Each request gets its own session.

---

# Step 3: Create a Model

`models.py`

```python
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
```

### SQL Equivalent

```sql
CREATE TABLE todos(
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT
);
```

Python classes become database tables.

---

# Step 4: Pydantic Schema

`schemas.py`

```python
class TodoCreate(BaseModel):
    title: str
    description: str
```

Don't confuse SQLAlchemy with Pydantic.

| SQLAlchemy | Pydantic |
|------------|----------|
| Stores data | Validates data |
| Database layer | API layer |
| `Column()` | `BaseModel` |

---

# Step 5: CRUD Operations

## Create

```python
db.add(new_todo)
db.commit()
db.refresh(new_todo)
```

### Flow

```text
Python Object
     │
db.add()
     │
db.commit()
     │
SQLite
```

### Why `refresh()`?

After inserting, SQLAlchemy fetches generated values like `id`.

---

## Read

```python
db.query(Todo).all()
```

SQL:

```sql
SELECT * FROM todos;
```

---

## Read One

```python
db.query(Todo).filter(Todo.id == 1).first()
```

SQL:

```sql
SELECT * FROM todos
WHERE id = 1
LIMIT 1;
```

---

## Update

```python
existing.title = todo.title
db.commit()
```

Changes become permanent only after `commit()`.

---

## Delete

```python
db.delete(todo)
db.commit()
```

SQL:

```sql
DELETE FROM todos;
```

---

# Dependency Injection

```python
db: Session = Depends(get_db)
```

FastAPI automatically:

- Creates a database session
- Passes it to the route
- Closes it after the request

Without Dependency Injection:

```python
db = SessionLocal()

# use database

db.close()
```

With Dependency Injection:

```python
db: Session = Depends(get_db)
```

Cleaner and safer.

---

# SQLAlchemy Cheat Sheet

| SQLAlchemy | SQL Equivalent |
|------------|---------------|
| `db.add()` | INSERT |
| `db.query()` | SELECT |
| `.filter()` | WHERE |
| `.first()` | LIMIT 1 |
| `.all()` | SELECT ALL |
| `db.commit()` | COMMIT |
| `db.refresh()` | Reload Row |
| `db.delete()` | DELETE |

---

# Running the Project

Install dependencies.

```bash
pip install fastapi uvicorn sqlalchemy
```

Run the server.

```bash
uvicorn app:app --reload
```

Open Swagger.

```text
http://127.0.0.1:8000/docs
```

---

# Common Beginner Mistakes

### Forgetting `commit()`

❌ Wrong

```python
db.add(todo)
```

Nothing gets saved.

✅ Correct

```python
db.add(todo)
db.commit()
```

---

### Forgetting `refresh()`

Without `refresh()`, generated values like `id` may not appear immediately.

---

### Using One Global Session

❌ Wrong

```python
db = SessionLocal()
```

This shares the same session.

✅ Correct

```python
db: Session = Depends(get_db)
```

Each request gets a fresh session.

---

# Interview Questions

## Beginner Level

### 1. What is SQLAlchemy?

SQLAlchemy is a Python ORM that lets us interact with databases using Python classes instead of raw SQL.

---

### 2. What is an ORM?

An ORM maps:

- Python Class → Database Table
- Python Object → Database Row
- Attribute → Column

---

### 3. What does `create_engine()` do?

It creates the connection between SQLAlchemy and the database.

---

### 4. Why do we use `declarative_base()`?

It creates a base class that every SQLAlchemy model inherits from.

Without it, SQLAlchemy cannot create tables from Python classes.

---

### 5. Difference between SQLAlchemy Model and Pydantic Model?

| SQLAlchemy | Pydantic |
|------------|----------|
| Database | API |
| Stores data | Validates data |
| `Column()` | `BaseModel` |

---

## Intermediate Level

### 6. What is `SessionLocal`?

It is a factory that creates database sessions.

Each request should receive its own session.

---

### 7. Why use `Depends(get_db)`?

It automatically creates and closes database sessions, preventing connection leaks.

---

### 8. Difference between `add()` and `commit()`?

- `add()` stages the object.
- `commit()` permanently saves it.

Think of `add()` as placing a letter in a mailbox and `commit()` as sending it.

---

### 9. Why use `refresh()`?

It reloads the object from the database and retrieves generated values like auto-increment IDs.

---

### 10. Difference between `first()` and `all()`?

| Method | Returns |
|---------|---------|
| `first()` | One object |
| `all()` | List of objects |

---

## Advanced Level

### 11. Why is `check_same_thread=False` needed for SQLite?

SQLite normally allows only the thread that created the connection to use it.

FastAPI handles multiple requests concurrently, so this setting allows SQLAlchemy to work correctly with separate sessions.

---

### 12. What happens if we don't close sessions?

Database connections remain open, eventually exhausting available connections.

Using `Depends(get_db)` solves this problem.

---

### 13. How does SQLAlchemy convert Python code into SQL?

Example:

```python
db.query(Todo).filter(Todo.id == 1).first()
```

Generated SQL:

```sql
SELECT * FROM todos
WHERE id = 1
LIMIT 1;
```

SQLAlchemy builds these SQL statements internally.

---

# Quick Revision (30 Seconds)

- `create_engine()` connects SQLAlchemy to SQLite.
- `SessionLocal` creates database sessions.
- `Base` is the parent class for all models.
- SQLAlchemy models become database tables.
- Pydantic validates API data.
- `db.add()`, `db.commit()`, `db.refresh()` insert records.
- `Depends(get_db)` automatically manages sessions.
- `first()` returns one record, while `all()` returns a list.

---
