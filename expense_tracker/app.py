from contextlib import asynccontextmanager

from fastapi import FastAPI

from .dependencies import create_db_and_tables
from .routers import expenses, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(expenses.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.get("/")
async def root():
    return "I'm just a placeholder"
