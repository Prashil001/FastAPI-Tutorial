from sqlalchemy.orm import Session
from models import Todo



## create operation
def create_todo(db: Session, todo):
    new_todo = Todo(
        title = todo.title,
        description = todo.description
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

## Read All
def get_todos(db: Session):
    return db.query(Todo).all()


## Read One Row
def get_todo(db: Session, todo_id : int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


## Update
def update_todo(db: Session, todo_id: int, todo):
    existing = db.query(Todo).filter(Todo.id == todo_id).first()

    if existing:
        existing.title = todo.title
        existing.description = todo.description

        db.commit()
        db.refresh(existing)

    return existing


## delete
def delete_todo(db: Session, todo_id:int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo:
        db.delete(todo)
        db.commit()

    return todo


