from fastapi import FastAPI
from app.api.v1.router import api_router

from app.db.database import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API", "docs": "/docs", "base": "/api/v1"}


app.include_router(api_router, prefix="/api/v1")