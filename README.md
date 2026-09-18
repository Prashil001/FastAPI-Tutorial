# SQLAlchemy Basics with FastAPI

> Learn how to integrate SQLAlchemy 2.0 with FastAPI using SQLite. This chapter covers database connections, models, sessions, CRUD operations, and dependency injection.

## What You'll Learn

* What is SQLAlchemy?

* Why use an ORM?

* Setting up SQLite with SQLAlchemy

* Creating the database engine

* Creating models

* Database sessions

* CRUD operations

* Dependency Injection with `Depends(get_db)`

* Common interview questions

# Project Structure

```
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

# What is SQLAlchemy?

SQLAlchemy is Python's most popular ORM (Object Relational Mapper).

Instead of writing SQL queries manually, you interact with the database using Python classes and objects.

Without SQLAlchemy:

SQL

```
INSERT INTO todos(title, description)
VALUES ('Learn SQLAlchemy', 'Practice ORM');
```

With SQLAlchemy:

Python

Run

```
todo = Todo(
    title="Learn SQLAlchemy",
    description="Practice ORM"
)

db.add(todo)
db.commit()
```

Much cleaner and easier to maintain.

# What is an ORM?

ORM stands for Object Relational Mapper.

It maps:

|
Python

|

Database

|
| --- | --- |
|

Class

|

Table

|
|

Object

|

Row

|
|

Attribute

|

Column

|

Example:

Python

Run

```
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
```

becomes

|
id

|

title

|
| --- | --- |
|

1

|

Learn FastAPI

|
|

2

|

Study SQLAlchemy

|

# Why Use SQLAlchemy?

|
Without ORM

|

With ORM

|
| --- | --- |
|

Write SQL manually

|

Write Python code

|
|

More repetitive

|

Cleaner

|
|

Harder to maintain

|

Easier

|
|

Less reusable

|

More reusable

|

# Architecture

![](data\:image/svg+xml;charset=utf-8,%3Csvg%20font-family%3D%22-apple-system-body%2C%20ui-sans-serif%2C%20-apple-system%2C%20system-ui%2C%20%26quot%3BSegoe%20UI%26quot%3B%2C%20Helvetica%2C%20%26quot%3BApple%20Color%20Emoji%26quot%3B%2C%20Arial%2C%20sans-serif%2C%20%26quot%3BSegoe%20UI%20Emoji%26quot%3B%2C%20%26quot%3BSegoe%20UI%20Symbol%26quot%3B%22%20font-weight%3D%22400%22%20data-d-component%3D%22svg%22%20fill%3D%22currentColor%22%20height%3D%22170%22%20style%3D%22color%3Argb\(13%2C%2013%2C%2013\)%22%20viewBox%3D%220%200%20820%20170%22%20width%3D%22100%25%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20x%3D%2220%22%20y%3D%2260%22%20width%3D%22140%22%20height%3D%2250%22%20rx%3D%2212%22%20fill%3D%22none%22%20stroke%3D%22currentColor%22%20stroke-width%3D%222%22%2F%3E%3Ctext%20x%3D%2290%22%20y%3D%2290%22%20text-anchor%3D%22middle%22%20font-size%3D%2216%22%3EClient%3C%2Ftext%3E%3Cpath%20d%3D%22M160%2085%20L280%2085%22%20stroke%3D%22currentColor%22%20stroke-width%3D%222%22%20fill%3D%22none%22%2F%3E%3Cpolygon%20points%3D%22280%2C85%20265%2C77%20265%2C93%22%20fill%3D%22currentColor%22%2F%3E%3Crect%20x%3D%22280%22%20y%3D%2235%22%20width%3D%22180%22%20height%3D%22100%22%20rx%3D%2212%22%20fill%3D%22none%22%20stroke%3D%22currentColor%22%20stroke-width%3D%222%22%2F%3E%3Ctext%20x%3D%22370%22%20y%3D%2260%22%20text-anchor%3D%22middle%22%20font-size%3D%2216%22%3EFastAPI%3C%2Ftext%3E%3Ctext%20x%3D%22370%22%20y%3D%2282%22%20text-anchor%3D%22middle%22%20font-size%3D%2213%22%3EDepends\(get_db\)%3C%2Ftext%3E%3Ctext%20x%3D%22370%22%20y%3D%22102%22%20text-anchor%3D%22middle%22%20font-size%3D%2213%22%3ECRUD%20Functions%3C%2Ftext%3E%3Cpath%20d%3D%22M460%2085%20L580%2085%22%20stroke%3D%22currentColor%22%20stroke-width%3D%222%22%20fill%3D%22none%22%2F%3E%3Cpolygon%20points%3D%22580%2C85%20565%2C77%20565%2C93%22%20fill%3D%22currentColor%22%2F%3E%3Crect%20x%3D%22580%22%20y%3D%2235%22%20width%3D%22220%22%20height%3D%22100%22%20rx%3D%2212%22%20fill%3D%22none%22%20stroke%3D%22currentColor%22%20stroke-width%3D%222%22%2F%3E%3Ctext%20x%3D%22690%22%20y%3D%2260%22%20text-anchor%3D%22middle%22%20font-size%3D%2216%22%3ESQLAlchemy%3C%2Ftext%3E%3Ctext%20x%3D%22690%22%20y%3D%2282%22%20text-anchor%3D%22middle%22%20font-size%3D%2213%22%3EEngine%20%E2%86%92%20Session%3C%2Ftext%3E%3Ctext%20x%3D%22690%22%20y%3D%22102%22%20text-anchor%3D%22middle%22%20font-size%3D%2213%22%3ESQLite%20\(test.db\)%3C%2Ftext%3E%3C%2Fsvg%3E)

# Step 1: Database Connection

`database.py`

Python

Run

```
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

### What is `create_engine()`?

The engine is SQLAlchemy's bridge between your application and the database.

Think of it as:

```
FastAPI
   │
Engine
   │
SQLite
```

It knows:

* where the database is

* how to connect

* how to execute SQL

# Step 2: Session

Python

Run

```
SessionLocal = sessionmaker(...)
```

A session represents one conversation with the database.

Every request gets its own session.

Example:

```
Request 1 → Session A
Request 2 → Session B
Request 3 → Session C
```

This prevents requests from interfering with each other.

# Step 3: Base Class

Python

Run

```
Base = declarative_base()
```

Every SQLAlchemy model inherits from `Base`.

Example:

Python

Run

```
class Todo(Base):
```

Without `Base`, SQLAlchemy won't recognize your model as a table.

# Step 4: Models

`models.py`

Python

Run

```
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
```

### SQL Equivalent

SQL

```
CREATE TABLE todos(
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT
);
```

Notice how Python replaces SQL.

# Step 5: Pydantic Schema

`schemas.py`

Python

Run

```
class TodoCreate(BaseModel):
    title: str
    description: str
```

Important distinction:

|
SQLAlchemy

|

Pydantic

|
| --- | --- |
|

Stores data

|

Validates data

|
|

Database

|

API

|
|

`Column()`

|

`BaseModel`

|

# Step 6: CRUD Operations

## Create

Python

Run

```
db.add(new_todo)
db.commit()
db.refresh(new_todo)
```

Flow:

```
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

Example:

Before refresh:

Python

Run

```
new_todo.id
```

may not contain the latest value.

After refresh:

Python

Run

```
new_todo.id = 1
```

## Read

Python

Run

```
db.query(Todo).all()
```

SQL:

SQL

```
SELECT * FROM todos;
```

Single record:

Python

Run

```
db.query(Todo).filter(Todo.id == 1).first()
```

SQL:

SQL

```
SELECT * FROM todos
WHERE id = 1
LIMIT 1;
```

## Update

Python

Run

```
existing.title = todo.title

db.commit()
```

Changes become permanent only after `commit()`.

## Delete

Python

Run

```
db.delete(todo)
db.commit()
```

Equivalent SQL:

SQL

```
DELETE FROM todos;
```

# Dependency Injection

Python

Run

```
db: Session = Depends(get_db)
```

This is one of the most important FastAPI concepts.

Without Dependency Injection:

Python

Run

```
db = SessionLocal()

# use database

db.close()
```

Every route would repeat this.

With FastAPI:

Python

Run

```
db: Session = Depends(get_db)
```

FastAPI automatically:

1. creates the session

2. gives it to your route

3. closes it afterward

# CRUD Cheat Sheet

|
SQLAlchemy

|

SQL

|
| --- | --- |
|

`db.add()`

|

INSERT

|
|

`db.query()`

|

SELECT

|
|

`.filter()`

|

WHERE

|
|

`.first()`

|

LIMIT 1

|
|

`.all()`

|

SELECT ALL

|
|

`db.commit()`

|

COMMIT

|
|

`db.refresh()`

|

Reload row

|
|

`db.delete()`

|

DELETE

|

# Running the Project

Install dependencies.

Bash

```
pip install fastapi uvicorn sqlalchemy
```

Run the server.

Bash

```
uvicorn app:app --reload
```

Open Swagger.

```
http://127.0.0.1:8000/docs
```

# Common Beginner Mistakes

### Forgetting `commit()`

Wrong:

Python

Run

```
db.add(todo)
```

The data won't be saved.

Correct:

Python

Run

```
db.add(todo)
db.commit()
```

### Forgetting `refresh()`

Without `refresh()`:

Python

Run

```
todo.id
```

may not contain the latest database value.

### Using One Session Everywhere

Don't create one global session.

Wrong:

Python

Run

```
db = SessionLocal()
```

Better:

Python

Run

```
Depends(get_db)
```

Each request gets its own session.

# Interview Questions

## Beginner Level

### 1. What is SQLAlchemy?

Answer:

SQLAlchemy is a Python ORM that lets us interact with databases using Python classes instead of writing raw SQL.

### 2. What is an ORM?

An ORM maps:

* Python class → Database table

* Python object → Database row

* Attribute → Column

### 3. What is `create_engine()`?

It creates the connection between SQLAlchemy and the database.

### 4. Why do we use `declarative_base()`?

It creates a base class that every SQLAlchemy model inherits from.

Without it, SQLAlchemy cannot create tables from Python classes.

### 5. Difference between SQLAlchemy Model and Pydantic Model?

|
SQLAlchemy

|

Pydantic

|
| --- | --- |
|

Database

|

API

|
|

Stores data

|

Validates data

|
|

`Column()`

|

`BaseModel`

|

## Intermediate Level

### 6. What is `SessionLocal`?

It is a factory that creates database sessions.

Each request should receive its own session.

### 7. Why use `Depends(get_db)`?

It automatically creates and closes database sessions, preventing connection leaks.

### 8. Difference between `add()` and `commit()`?

* `add()` stages the object.

* `commit()` permanently saves it.

Think of `add()` as placing a letter in the mailbox and `commit()` as sending it.

### 9. Why use `refresh()`?

It reloads the object from the database and retrieves generated values like auto-increment IDs.

### 10. Difference between `first()` and `all()`?

|
Method

|

Returns

|
| --- | --- |
|

`first()`

|

One object

|
|

`all()`

|

List of objects

|

## Advanced Interview Questions

### 11. Why is `check_same_thread=False` needed for SQLite?

SQLite normally allows only the thread that created the connection to use it.

FastAPI handles multiple requests concurrently, so this setting allows SQLAlchemy to reuse the connection safely with separate sessions.

### 12. What happens if we don't close sessions?

Database connections remain open, eventually exhausting available connections and causing application failures.

Using `Depends(get_db)` solves this.

### 13. How does SQLAlchemy convert Python code into SQL?

SQLAlchemy builds SQL statements internally.

Example:

Python

Run

```
db.query(Todo).filter(Todo.id == 1).first()
```

becomes

SQL

```
SELECT * FROM todos
WHERE id = 1
LIMIT 1;
```

# Quick Revision (30 Seconds)

* SQLAlchemy is Python's most popular ORM.

* `create_engine()` connects to the database.

* `SessionLocal` creates database sessions.

* `Base` is the parent class for all models.

* Models represent tables.

* Pydantic validates API data.

* `db.add()`, `db.commit()`, `db.refresh()` insert records.

* `Depends(get_db)` automatically manages database sessions.

* `first()` returns one record, while `all()` returns a list.

* `commit()` saves changes permanently.


