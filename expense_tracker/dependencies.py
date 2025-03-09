from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from sqlmodel import Session, create_engine, SQLModel

from config import db_uri


connect_args = {"check_same_thread": False}
engine = create_engine(db_uri(), connect_args=connect_args)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db_session():
    with Session(engine) as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_db_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
