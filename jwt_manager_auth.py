import os
from datetime import timedelta, datetime
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from config.database import SessionLocal
from models.users_model import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# Constant to raise if could not validate credentials.
CREDENTIALS_EXCEPTION = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate user : (", 
            headers={"WWW-Authenticate": "Bearer"})


router = APIRouter(prefix="/auth", tags=["Authentication"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db, username: str, password: str):
    """ Check if username and password matches with database information. """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user


def create_access_token(username: str, user_id: int, token_expires: timedelta):
    """ Generate unique token if user has logged in successfully. """
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + token_expires
    encode.update({"exp": expires})

    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username == None or user_id == None:
            raise CREDENTIALS_EXCEPTION
        
        return {"username": username, "id": user_id}
    except JWTError:
        raise CREDENTIALS_EXCEPTION


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user: CreateUserRequest):
    """ Create new user and store it in the database. """
    create_user_model = Users(
        username=create_user.username,
        hashed_password=bcrypt_context.hash(create_user.password))
    
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency):
    """ Token endpoint will return a token after all validations were completed. """
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise CREDENTIALS_EXCEPTION
    
    token = create_access_token(user.username, user.id, timedelta(minutes=3))

    return {"access_token": token, "token_type": "bearer"}


