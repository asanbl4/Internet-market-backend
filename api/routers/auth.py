import datetime
import os
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api import crud, schemas, deps
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta

load_dotenv()

router = APIRouter(prefix='/auth', tags=["auth"])

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES=30


def authenticate_user(username: str, password: str, db: deps.db_dependency):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not deps.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/')
async def create_user(db: deps.db_dependency, user_create: schemas.UserCreate):
    return crud.create_user(db, user_create)


@router.get('/get')
async def get_users(db: deps.db_dependency):
    return crud.get_all_users(db)


@router.post('/token')
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: deps.db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return schemas.Token(
        access_token=access_token,
        token_type="Bearer"
    )





