from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from config import db_uri


engine = create_engine(db_uri())


def get_db_session():
    with Session(engine) as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_db_session)]
