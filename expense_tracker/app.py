from contextlib import asynccontextmanager

from fastapi import FastAPI

from .dependencies import create_db_and_tables
from .routers import expenses


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(expenses.router)

@app.get("/")
async def root():
    return "I'm just a placeholder"
