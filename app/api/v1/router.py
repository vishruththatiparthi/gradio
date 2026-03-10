from fastapi import APIRouter
from app.api.v1.endpoints import health, todo, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(todo.router, prefix="/todos", tags=["Todos"])
