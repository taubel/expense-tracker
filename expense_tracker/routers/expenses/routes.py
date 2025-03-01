from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from ...dependencies import DBSessionDep
from .models import Expense, ExpenseCreate, ExpensePublic


router = APIRouter(prefix="/expenses")


@router.get("/", response_model=list[ExpensePublic])
async def get_all_expenses(session: DBSessionDep, offset: int = 0, limit: int = Query(default=100, le=100)):
    expenses = session.exec(select(Expense).offset(offset).limit(limit)).all()
    return expenses


@router.get("/{item_id}", response_model=ExpensePublic)
async def get_expense(item_id: int, session: DBSessionDep):
    expense = session.get(Expense, item_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("/", response_model=ExpensePublic)
async def add_expense(expense: ExpenseCreate, session: DBSessionDep):
    expense = Expense.model_validate(expense)
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


@router.put("/{item_id}", response_model=ExpensePublic)
async def update_expense(item_id: int, expense: ExpenseCreate, session: DBSessionDep):
    db_expense = session.get(Expense, item_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    data = expense.model_dump()
    db_expense.sqlmodel_update(data)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense
