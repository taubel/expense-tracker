from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Form
from fastapi.responses import RedirectResponse
from sqlmodel import select

from ...dependencies import DBSessionDep, hash_password
from .models import User, UserCreate, UserPublic


router = APIRouter(prefix="/users")


@router.post("/", response_model=UserPublic)
async def add_user(user: UserCreate, session: DBSessionDep):
    existing_user = session.exec(select(User).where(User.name == user.name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    user = User.model_validate(user, update={"hashed_password": hashed_password})

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/form", response_model=UserPublic)
async def add_user_form(name: Annotated[str, Form()], password: Annotated[str, Form()], session: DBSessionDep):
    existing_user = session.exec(select(User).where(User.name == name)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(password)
    user = User(name=name, hashed_password=hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return RedirectResponse("/login", status_code=303)


@router.get("/{item_id}", response_model=UserPublic)
async def get_user(item_id: int, session: DBSessionDep):
    user = session.get(User, item_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")
    return user


@router.get("/", response_model=list[UserPublic])
async def get_all_users(session: DBSessionDep):
    users = session.exec(select(User)).all()
    return users


@router.delete("/{item_id}")
async def delete_user(item_id: int, session: DBSessionDep):
    user = session.get(User, item_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")
    session.delete(user)
    session.commit()


@router.put("/{item_id}", response_model=UserPublic)
async def update_user(item_id: int, user: UserCreate, session: DBSessionDep):
    db_user = session.get(User, item_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User not found")
    data = user.model_dump()
    db_user.sqlmodel_update(data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
