from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List

from starlette.requests import Request
from jwt_manager_auth import validate_token, create_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
#Update the title of our API.
app.title = "Basic API"
#Also, we can modify its actual version.
app.version = "0.0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "johndoe@example.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")

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
    nombre: str = Field(min_length=3, max_length=15)
    año: int = Field(le=2022)
    categoria: str
    reseñas: float

    class Config:
        #Seems like the name always should be schema_extra in order to represent an example.
        schema_extra = {
            "example": {
                "id": 5,
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

#We can modify what kind of response should give the API.
@app.get('/movies', tags=["Peliculas, chicles, tance"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer)])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

# User auth
@app.post('/login', tags=["Auth"], status_code=200, response_model=User)
def auth_user(user: User) -> User:
    if user.email == "johndoe@example.com" and user.password == "*****":
        token: str = create_token(dict(user))
        return JSONResponse(content=token)
    return user


#Get movie by id.
@app.get('/movies/{id}', tags=["Peliculas, chicles, tance"], response_model=Movie, status_code=200)
#Set up id in the function parameter and specify its type. ge <- mininum, and le <- maximum. 
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    #Iterate dictionary.
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
        else:
            raise HTTPException(status_code=404, detail="Ni un brillo pelao, busca otro id")
    return JSONResponse("Ni un brillo pelao")

""" Ya se pudo :D con parametros query"""
@app.get('/name/', tags=["Peliculas, chicles, tance"], response_model=List[Movie])
def get_movie_by_name(nombre: str, year: int, category: str) -> List[Movie]:

    categories = [cat for cat in movies if cat["categoria"] == category]
    if categories not in movies:
        raise HTTPException(status_code=404, detail="Mani esa pelicula no existe")
    return nombre, year, categories


@app.get('/movies/', tags=["Peliculas, chicles, tance"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)):
    for cat in movies:
        if cat["categoria"] == category:
            return JSONResponse(content=cat)
    return "Ni un brillo pelao"


#POST method
@app.post('/movies', tags=["Peliculas, chicles, tance"], response_model=dict, status_code=201)
def post_movie(movie: Movie) -> dict:
    
    movies.append(movie)

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
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return JSONResponse(content={"message": "Se ha eliminado la pelicula..."})
