from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Pydantic Model
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


# Fake Database
todos = []


# CREATE
@app.post("/todos")
def create_todo(todo: Todo):
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }

    todos.append(new_todo)
    return {"message": "Todo created", "todo": new_todo}


# READ ALL
@app.get("/todos")
def get_all_todos():
    return todos


# READ ONE
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")


# UPDATE
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = updated_todo.title
            todo["completed"] = updated_todo.completed
            return {"message": "Todo updated", "todo": todo}

    raise HTTPException(status_code=404, detail="Todo not found")


# DELETE
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return {"message": "Todo deleted"}

    raise HTTPException(status_code=404, detail="Todo not found")