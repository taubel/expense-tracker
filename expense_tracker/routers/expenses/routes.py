from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ...dependencies import DBSessionDep
from .models import Expense


router = APIRouter(prefix="/expenses")


# TODO add query parameters
@router.get("/")
async def get_all_expenses(session: DBSessionDep) -> list[Expense]:
    expenses = session.exec(select(Expense))
    return expenses


@router.get("/{item_id}")
async def get_expense(item_id: int, session: DBSessionDep) -> Expense:
    expense = session.get(Expense, item_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("/")
async def add_expense(expense: Expense, session: DBSessionDep) -> Expense:
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


@router.delete("/{item_id}")
async def delete_expense(item_id: int, session: DBSessionDep):
    expense = session.get(Expense, item_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    session.delete(expense)
    session.commit()
