from datetime import datetime

from fastapi.testclient import TestClient
from sqlmodel import Session

from expense_tracker.routers.expenses.models import Expense
from expense_tracker.routers.users.models import User


def test_add_expense(client: TestClient, user: User):
    response = client.post("/api/expenses", json={
        "amount": 1.0,
        "user_id": user.id,
        "timestamp": datetime.now().isoformat()
    })

    assert response.status_code == 200


def test_add_expense_missing_amount(client: TestClient, user: User):
    response = client.post("/api/expenses", json={
        "user_id": user.id,
        "timestamp": datetime.now().isoformat()
    })

    assert response.status_code == 422


def test_get_all_expenses(session: Session, client: TestClient, user: User):
    expense1 = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    expense2 = Expense(amount=2.5, user_id=user.id, timestamp=datetime.now())
    session.add(expense1)
    session.add(expense2)
    session.commit()

    response = client.get("/api/expenses")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["amount"] == expense1.amount
    assert data[0]["user_id"] == user.id
    assert data[0]["timestamp"] == expense1.timestamp.isoformat()
    assert data[0]["id"] == expense1.id
    assert data[1]["amount"] == expense2.amount
    assert data[1]["user_id"] == user.id
    assert data[1]["timestamp"] == expense2.timestamp.isoformat()
    assert data[1]["id"] == expense2.id


def test_get_all_expenses_limit_first(session: Session, client: TestClient, user: User):
    expense1 = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    expense2 = Expense(amount=2.5, user_id=user.id, timestamp=datetime.now())
    session.add(expense1)
    session.add(expense2)
    session.commit()

    response = client.get("/api/expenses", params={"offset": 0, "limit": 1})
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["amount"] == expense1.amount
    assert data[0]["user_id"] == user.id
    assert data[0]["timestamp"] == expense1.timestamp.isoformat()
    assert data[0]["id"] == expense1.id


def test_get_all_expenses_limit_second(session: Session, client: TestClient, user: User):
    expense1 = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    expense2 = Expense(amount=2.5, user_id=user.id, timestamp=datetime.now())
    session.add(expense1)
    session.add(expense2)
    session.commit()

    response = client.get("/api/expenses", params={"offset": 1, "limit": 1})
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["amount"] == expense2.amount
    assert data[0]["user_id"] == user.id
    assert data[0]["timestamp"] == expense2.timestamp.isoformat()
    assert data[0]["id"] == expense2.id


def test_get_expense(session: Session, client: TestClient, user: User):
    expense = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    session.add(expense)
    session.commit()

    response = client.get(f"/api/expenses/{expense.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["amount"] == expense.amount
    assert data["user_id"] == user.id
    assert data["timestamp"] == expense.timestamp.isoformat()
    assert data["id"] == expense.id


def test_get_expense_non_existing(session: Session, client: TestClient):
    response = client.get(f"/api/expenses/0")

    assert response.status_code == 404


def test_delete_expense(session: Session, client: TestClient, user: User):
    expense = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    session.add(expense)
    session.commit()

    response = client.delete(f"/api/expenses/{expense.id}")
    assert response.status_code == 200

    expense_in_db = session.get(Expense, expense.id)
    assert expense_in_db is None


def test_update_expense(session: Session, client: TestClient, user: User):
    expense = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    session.add(expense)
    session.commit()

    response = client.put(f"/api/expenses/{expense.id}", json={
        "amount": 2.0,
        "user_id": user.id,
        "timestamp": expense.timestamp.isoformat(),
    })
    data = response.json()

    assert response.status_code == 200
    assert data["amount"] == 2.0


def test_update_expense_missing_amount(session: Session, client: TestClient, user: User):
    expense = Expense(amount=1.0, user_id=user.id, timestamp=datetime.now())
    session.add(expense)
    session.commit()

    response = client.put(f"/api/expenses/{expense.id}", json={
        "user_id": user.id,
        "timestamp": expense.timestamp.isoformat(),
    })

    assert response.status_code == 422
