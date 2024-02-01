from fastapi import APIRouter, Path, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette import status
from typing import Optional, List, Annotated

from fastapi.encoders import jsonable_encoder
from config.database import SessionLocal
from models.movie import Movie as MovieModel
from jwt_manager_auth import oauth2_bearer


DB = SessionLocal()
ID_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie ID : (")

movies_router = APIRouter()


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



#We can modify what kind of response should give the API.
@movies_router.get('/movies', tags=["Peliculas, chicles, tance"], response_model=List[Movie], status_code=200)
def get_movies(token: Annotated[str, Depends(oauth2_bearer)]) -> List[Movie]:
    
    result = DB.query(MovieModel).all()
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


#Get movie by id.
@movies_router.get('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=Movie, status_code=200)
#Set up id in the function parameter and specify its type. ge <- mininum, and le <- maximum. 
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:

    output_movie = DB.query(MovieModel).filter(id == MovieModel.id).first()
    
    if not output_movie:
        raise ID_EXCEPTION
      
    return jsonable_encoder(output_movie)


""" Ya se pudo :D con parametros query"""
@movies_router.get('/name/', tags=["Peliculas, chicles, tance"], response_model=List[Movie])
def get_movie_by_name(nombre: str,) -> Movie:

    output_movie = DB.query(MovieModel).filter(nombre == MovieModel.nombre).first()

    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie name : (")
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)


@movies_router.get('/movies/', tags=["Peliculas, chicles, tance"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)):
    
    output_movie = DB.query(MovieModel).filter(category == MovieModel.categoria).first()

    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie category : (")
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)


#POST method
@movies_router.post('/movies', tags=["Peliculas, chicles, tance"], response_model=dict, status_code=201)
def post_movie(movie: Movie) -> dict:

    new_movie = MovieModel(**movie.dict())
    DB.add(new_movie)
    DB.commit()

    return JSONResponse(content={"message": "Se ha registrado la pelicula..."}, status_code=201)


#PUT method
@movies_router.put('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=dict)
#Specify which items would you like to update
def update_movie(id: int, movie: Movie) -> dict:

    movie_to_update = DB.query(MovieModel).filter(id == MovieModel.id).first()

    if not movie_to_update:
        raise ID_EXCEPTION
    
    movie_to_update.nombre = movie.nombre
    movie_to_update.año = movie.año
    movie_to_update.categoria = movie.categoria
    movie_to_update.reseñas = movie.reseñas
    DB.commit()

    return JSONResponse(content={"message": "Se ha actualizado la pelicula..."}, status_code=status.HTTP_202_ACCEPTED)

    
@movies_router.delete('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=dict)
def delete_movie(id: int, token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    
    movie_to_delete = DB.query(MovieModel).filter(id == MovieModel.id).first()

    if not movie_to_delete:
        raise ID_EXCEPTION
    
    DB.delete(movie_to_delete)
    DB.commit()

    return JSONResponse(content={"message": "Se ha eliminado la pelicula..."}, status_code=status.HTTP_200_OK)

