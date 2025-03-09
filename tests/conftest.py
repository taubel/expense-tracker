from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from expense_tracker import app
from expense_tracker.dependencies import get_db_session
from expense_tracker.routers.users.models import User


@pytest.fixture(scope="function")
def session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def user(session: Session):
    user = User(name="Tester", hashed_password="qwerty")
    session.add(user)
    session.commit()
    session.refresh(user)
    yield user
    session.delete(user)
    session.commit()
