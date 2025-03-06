from fastapi.testclient import TestClient
from sqlmodel import Session

from expense_tracker.routers.users.models import User
from tests.conftest import session


def test_add_user(session: Session, client: TestClient):
    password = "qwerty"
    response = client.post("/api/users", json={
        "name": "Tester",
        "password": password,
    })
    data = response.json()

    assert response.status_code == 200

    user_in_db = session.get(User, data["id"])
    assert user_in_db.hashed_password != password


def test_add_user_missing_name(client: TestClient):
    response = client.post("/api/users", json={
        "password": "qwerty",
    })

    assert response.status_code == 422


def test_get_user(session: Session, client: TestClient):
    password = "hashedqwerty"
    user = User(name="Tester", hashed_password=password)
    session.add(user)
    session.commit()

    response = client.get(f"/api/users/{user.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == user.name
    assert data["id"] == user.id


def test_get_user_non_existing(client: TestClient):
    response = client.get(f"/api/users/0")

    assert response.status_code == 404


def test_get_all_users(session: Session, client: TestClient):
    user1 = User(name="Tester", hashed_password="hashed1")
    user2 = User(name="Lester", hashed_password="hashed2")
    session.add(user1)
    session.add(user2)
    session.commit()

    response = client.get("/api/users")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == user1.name
    assert data[0]["id"] == user1.id
    assert data[1]["name"] == user2.name
    assert data[1]["id"] == user2.id


def test_delete_user(session: Session, client: TestClient):
    user = User(name="Tester", hashed_password="hashedqwerty")
    session.add(user)
    session.commit()

    response = client.delete(f"/api/users/{user.id}")
    assert response.status_code == 200

    user_in_db = session.get(User, user.id)
    assert user_in_db is None


def test_update_user(session: Session, client: TestClient):
    user = User(name="Tester", hashed_password="hashedqwerty")
    session.add(user)
    session.commit()

    response = client.put(f"/api/expenses/{user.id}", json={
        "name": "Lester",
        # TODO API should not have any way to retrieve plain password
        # "password": user.password,
    })
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Lester"


def test_update_user_missing_password(session: Session, client: TestClient):
    user = User(name="Tester", hashed_password="hashedqwerty")
    session.add(user)
    session.commit()

    response = client.put(f"/api/expenses/{user.id}", json={
        "name": "Lester",
    })

    assert response.status_code == 422


def test_update_non_existing_user(session: Session, client: TestClient):
    response = client.put(f"/api/expenses/0", json={
        "name": "Lester",
        # TODO API should not have any way to retrieve plain password
        # "password": user.password,
    })

    assert response.status_code == 404
