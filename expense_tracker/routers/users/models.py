from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    name: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    # TODO unresolved reference
    expenses: list["Expense"] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
