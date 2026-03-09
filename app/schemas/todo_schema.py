from pydantic import BaseModel


class TodoCreate(BaseModel):
    task: str


class TodoResponse(BaseModel):
    id: int
    task: str

    class Config:
        from_attributes = True