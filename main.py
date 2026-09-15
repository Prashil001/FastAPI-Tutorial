from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Todo List API")


# =======================================================
# Pydantic Models
# =======================================================

class TodoCreate(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    completed: bool | None = None


class Todo(BaseModel):
    id: int
    title: str
    completed: bool


# =======================================================
# Fake Database
# =======================================================

todos: list[Todo] = [
    Todo(id=1, title="Learn FastAPI", completed=False),
    Todo(id=2, title="Build Todo API", completed=True)
]


# =======================================================
# Helper Function
# =======================================================

def find_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None


# =======================================================
# CREATE
# =======================================================

@app.post(
    "/todos",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: TodoCreate):
    new_todo = Todo(
        id=len(todos) + 1,
        title=todo.title,
        completed=todo.completed
    )

    todos.append(new_todo)
    return new_todo


# =======================================================
# READ ALL
# =======================================================

@app.get("/todos", response_model=list[Todo])
def get_all_todos(
    completed: bool | None = Query(default=None)
):
    """
    Optional filtering:
    /todos
    /todos?completed=true
    """

    if completed is None:
        return todos

    return [todo for todo in todos if todo.completed == completed]


# =======================================================
# READ ONE
# =======================================================

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(
    todo_id: int = Path(gt=0)
):
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


# =======================================================
# UPDATE
# =======================================================

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    updated_data: TodoUpdate
):
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    if updated_data.title is not None:
        todo.title = updated_data.title

    if updated_data.completed is not None:
        todo.completed = updated_data.completed

    return todo


# =======================================================
# DELETE
# =======================================================

@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todos.remove(todo)