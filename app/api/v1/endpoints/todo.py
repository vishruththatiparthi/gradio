from fastapi import APIRouter, HTTPException
from app.services import todo_service

router = APIRouter()


@router.post("/")
async def create(task: str):
    return todo_service.create_todo(task)


@router.get("/")
async def read():
    return todo_service.get_todos()


@router.get("/{todo_id}")
async def read_by_id(todo_id: int):
    todo = todo_service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}")
async def update(todo_id: int, task: str):
    todo = todo_service.update_todo(todo_id, task)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}")
async def delete(todo_id: int):
    deleted = todo_service.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
