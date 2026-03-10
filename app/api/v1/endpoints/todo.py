from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas import todo_schema
from app.core.security import get_current_user

router = APIRouter()


@router.post("/todos", response_model=todo_schema.TodoResponse)
def create_todo(
    todo: todo_schema.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_todo = models.Todo(task=todo.task, owner_id=current_user.id)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/todos", response_model=list[todo_schema.TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()


@router.get("/todos/{todo_id}", response_model=todo_schema.TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/todos/{todo_id}", response_model=todo_schema.TodoResponse)
def update_todo(
    todo_id: int,
    updated: todo_schema.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.task = updated.task

    db.commit()
    db.refresh(todo)

    return todo


@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted"}