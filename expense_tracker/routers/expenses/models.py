from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from ..users.models import User


class ExpenseBase(SQLModel):
    amount: float
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    timestamp: datetime


class Expense(ExpenseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="expenses")


class ExpenseCreate(ExpenseBase):
    pass


class ExpensePublic(ExpenseBase):
    id: int
