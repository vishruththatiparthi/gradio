from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API ", "docs": "/docs", "base": "/api/v1"}


app.include_router(api_router, prefix="/api/v1")
