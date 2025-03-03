from datetime import datetime

from sqlmodel import SQLModel, Field


class ExpenseBase(SQLModel):
    amount: float
    user_name: str  # TODO link to user model
    timestamp: datetime


class Expense(ExpenseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ExpenseCreate(ExpenseBase):
    pass


class ExpensePublic(ExpenseBase):
    id: int
