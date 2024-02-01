from routers.jwt_manager_auth import oauth2_bearer, get_current_user
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import SessionLocal
from models.users_model import Users as UsersModel
from starlette import status
from typing import Annotated

DB = SessionLocal()

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", status_code=status.HTTP_200_OK)
def get_all_users(token: Annotated[str, Depends(oauth2_bearer)]):
    """ Retrieve user id and username """

    users_db = DB.query(UsersModel.id, UsersModel.username).all()

    return JSONResponse(content=jsonable_encoder(dict(users_db)), status_code=status.HTTP_200_OK)


@users_router.get("/me", status_code=200)
def user(current_user: Annotated[dict, Depends(get_current_user)]):
    """ Return current user logged in, if not found will raise HTTP exception. """

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found...", 
            headers={"WWW-Authenticate": "Bearer"})
    
    return {"user": current_user}

