from routers.jwt_manager_auth import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/me", status_code=200)
def user(current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found...", 
            headers={"WWW-Authenticate": "Bearer"})
    
    return {"user": current_user}

