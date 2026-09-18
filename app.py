from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import localsession, Base, engine

app = FastAPI()

Base.metadata.create_all(bind = engine)

def get_db():
    db = localsession()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos")
def create_todo(todo: schemas.CreateTodo, db: Session = Depends(get_db)):
    return crud.create_todo(db,todo)

@app.get("/todos")
def get_all(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.put("/todos")
def update_todo(todo: schemas.CreateTodo, todo_id: int, db: Session = Depends(get_db)):
    return crud.update_todo(db,todo_id,todo)

@app.delete("/todos")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db,todo_id)