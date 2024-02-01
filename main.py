from routers import movies, jwt_manager_auth, html_endpoints, users
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
app.include_router(html_endpoints.html_router)
app.include_router(users.users_router)

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

