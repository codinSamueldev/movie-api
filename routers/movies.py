from fastapi import APIRouter, Path, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette import status
from typing import Optional, List, Annotated

from fastapi.encoders import jsonable_encoder
from config.database import SessionLocal
from models.movie import Movie as MovieModel
from services.movie_services import MovieServices, GetMovieService
from schemas.movie_schema import Movie
from routers.jwt_manager_auth import oauth2_bearer


DB = SessionLocal()
ID_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie ID : (")

movies_router = APIRouter()


#We can modify what kind of response should give the API.
@movies_router.get('/movies', tags=["Peliculas, chicles, tance"], response_model=List[Movie], status_code=200)
def get_movies(token: Annotated[str, Depends(oauth2_bearer)]) -> List[Movie]:
    """ Retrieve all movies stored in database. """

    result = MovieServices(DB).get_movies()
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


#Get movie by id.
@movies_router.get('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=Movie, status_code=200)
#Set up id in the function parameter and specify its type. ge <- mininum, and le <- maximum. 
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    """ Retrieve movie based on movie ID """

    output_movie = GetMovieService(DB).get_movie(id)
    
    if not output_movie:
        raise ID_EXCEPTION
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)


""" Ya se pudo :D con parametros query"""
@movies_router.get('/name/', tags=["Peliculas, chicles, tance"], response_model=List[Movie])
def get_movie_by_name(nombre: str,) -> Movie:
    """ Retrieve movie based on movie name """
    
    output_movie = MovieServices(DB).get_movie_by_name_query(nombre)

    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie name : (")
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)


@movies_router.get('/movies/', tags=["Peliculas, chicles, tance"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)):
    """ Retrieve movie based on category """

    output_movie = MovieServices(DB).get_movie_by_category_query(category)

    if not output_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid movie category : (")
      
    return JSONResponse(content=jsonable_encoder(output_movie), status_code=status.HTTP_200_OK)


#POST method
@movies_router.post('/movies', tags=["Peliculas, chicles, tance"], response_model=dict, status_code=201)
def post_movie(movie: Movie) -> dict:
    """ Add new movie """

    MovieServices(DB).add_movie(movie)

    return JSONResponse(content={"message": "Se ha registrado la pelicula..."}, status_code=201)


#PUT method
@movies_router.put('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=dict)
#Specify which items would you like to update
def update_movie(id: int, movie: Movie) -> dict:
    """ Update movie parameters (name, year, category, rating) """

    movie_to_update = GetMovieService(DB).get_movie(id)

    if not movie_to_update:
        raise ID_EXCEPTION
    
    MovieServices(DB).update_a_movie(id, movie)

    return JSONResponse(content={"message": "Se ha actualizado la pelicula..."}, status_code=status.HTTP_202_ACCEPTED)

    
@movies_router.delete('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=dict)
def delete_movie(id: int, token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    """ Delete movie if movie ID found """
    
    movie_to_delete = GetMovieService(DB).get_movie(id)

    if not movie_to_delete:
        raise ID_EXCEPTION
    
    MovieServices(DB).delete_a_movie(id)

    return JSONResponse(content={"message": "Se ha eliminado la pelicula..."}, status_code=status.HTTP_200_OK)

