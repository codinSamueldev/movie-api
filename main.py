from routers import movies, jwt_manager_auth
from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from starlette import status
from typing import Any, Optional, List, Annotated

from fastapi.encoders import jsonable_encoder
from config.database import SessionLocal, engine, Base
from models.movie import Movie as MovieModel
from routers.jwt_manager_auth import oauth2_bearer, get_current_user
from middlewares.error_handler import ErrorHandler



app = FastAPI()
app.include_router(jwt_manager_auth.security_router)
app.include_router(movies.movies_router)
#Update the title of our API.
app.title = "Basic API"
#Also, we can modify its actual version.
app.version = "0.0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "*********"
            }
        }



#Tags=[] help us to separate each endpoint in the documentation so we can see, verify and test each endpoint.
@app.get('/', tags=["Casita"])
def message():
    return "Holiiii"


@app.get('/test')
def message():
    return {"Testeo": "Si funciona"}

#Return HTML code
@app.get('/html', tags=["HTML"])
def message():
    return HTMLResponse("""

    <h1>Al parecer, funciona.</h1>
    <figure>
        <div style="background: black; width: 35%; height: 51%; border-radius: 35%"></div>
    </figure> """)


@app.get("/users/me", tags=["Users"], status_code=200)
def user(current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found...", 
            headers={"WWW-Authenticate": "Bearer"})
    
    return {"user": current_user}

