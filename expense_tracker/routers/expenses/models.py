from datetime import datetime

from sqlmodel import SQLModel, Field


class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # TODO don't allow use to pass id
    amount: float
    user_name: str  # TODO link to user model
    timestamp: datetime
