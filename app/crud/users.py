from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from app.core.hashing import Hasher
from app.db.session import get_db
from app.models.users import User
from app.schemas.users import UserAddUpdate, UserCreate


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> User:
    user = get_user_by_email(email=email, db=db)
    if not Hasher.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"})
    return user


def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"})
    return user


def get_user(id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"})
    return user


def list_users(db: Session) -> List[User]:
    users = db.query(User).order_by(User.id).all()
    return users


def create_new_user(user: UserCreate, db: Session) -> bool:
    try:
        is_superuser = False if db.query(User).limit(1).all() else True
        user = User(
            email=user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            is_superuser=is_superuser,
            role=user.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )
    return True


def update_user(id: int, user: UserAddUpdate, db: Session) -> bool:
    try:
        _user = get_user(id=id, db=db)
        _user.email = user.email
        _user.role = user.role
        db.commit()
        db.refresh(_user)
    except:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )
    return True


def delete_user(id: int, db: Session) -> bool:
    try:
        user = get_user(id=id, db=db)
        db.delete(user)
        db.commit()
    except:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )
    return True
