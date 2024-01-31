import jwt_manager_auth
from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from starlette import status
from typing import Any, Coroutine, Optional, List, Annotated

from starlette.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.encoders import jsonable_encoder
from config.database import SessionLocal, engine, Base
from models.movie import Movie as MovieModel
from sqlalchemy.orm import Session
from jwt_manager_auth import oauth2_bearer, get_current_user


DB = SessionLocal()


app = FastAPI()
app.include_router(jwt_manager_auth.router)
#Update the title of our API.
app.title = "Basic API"
#Also, we can modify its actual version.
app.version = "0.0.0.1"

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


class Movie(BaseModel):
    #Set up atributtes
    id: Optional[int] = None
    #Validate data with Field() class.
    nombre: str = Field(min_length=3, max_length=90)
    año: int = Field()
    categoria: str
    reseñas: float

    class Config:
        #Seems like the name always should be schema_extra in order to represent an example.
        schema_extra = {
            "example": {
                "nombre": "Pelicula",
                "año": 2012,
                "categoria": "Tragico/Suspenso",
                "reseñas": 6.6
            }
        }

movies = [
    {
        "id" : 1,
        "nombre" : "Mi pobre angelito",
        "año" : 2003,
        "categoria" : "Humor/Risa/Comedia",
        "reseñas" : 9.9
    },
    {
        "id" : 2,
        "nombre" : "Avengers Endgame",
        "año" : 2018,
        "categoria" : "Acción/Sci-Fi/Tragedia",
        "reseñas" : 9
    },
    {
        "id" : 3,
        "nombre" : "Chicken Little",
        "año" : 2005,
        "categoria" : "Humor/Risa/Reflexion",
        "reseñas" : 10
    }
]


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


#We can modify what kind of response should give the API.
@app.get('/movies', tags=["Peliculas, chicles, tance"], response_model=List[Movie], status_code=200)
def get_movies(token: Annotated[str, Depends(oauth2_bearer)]) -> List[Movie]:
    
    result = DB.query(MovieModel).all()
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


#Get movie by id.
@app.get('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=Movie, status_code=200)
#Set up id in the function parameter and specify its type. ge <- mininum, and le <- maximum. 
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:

    output_movie = DB.query(MovieModel).filter(id == MovieModel.id).first()
    
    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie ID : (")
      
    return jsonable_encoder(output_movie)

""" Ya se pudo :D con parametros query"""
@app.get('/name/', tags=["Peliculas, chicles, tance"], response_model=List[Movie])
def get_movie_by_name(nombre: str,) -> Movie:

    output_movie = DB.query(MovieModel).filter(nombre == MovieModel.nombre).first()

    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie category : (")
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)



@app.get('/movies/', tags=["Peliculas, chicles, tance"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)):
    
    output_movie = DB.query(MovieModel).filter(category == MovieModel.categoria).first()

    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie category : (")
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)


#POST method
@app.post('/movies', tags=["Peliculas, chicles, tance"], response_model=dict, status_code=201)
def post_movie(movie: Movie) -> dict:

    DB = SessionLocal()
    new_movie = MovieModel(**movie.dict())
    DB.add(new_movie)
    DB.commit()

    # movies.append(movie)

    return JSONResponse(content={"message": "Se ha registrado la pelicula..."}, status_code=201)


#PUT method
@app.put('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=dict)
#Specify which items would you like to update
def update_movie(id: int, movie: Movie) -> dict:
    
    for item in movies:
        if item["id"] == id:
            item["nombre"] = movie.nombre
            item["año"] = movie.año
            item["categoria"] = movie.categoria
            item["reseñas"] = movie.reseñas
            return JSONResponse(content={"message": "Se ha actualizado la pelicula..."})
    return JSONResponse(content={"important message": "Ni un brillo pelao"})

    
@app.delete('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=dict)
def delete_movie(id: int, token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return JSONResponse(content={"message": "Se ha eliminado la pelicula..."})
