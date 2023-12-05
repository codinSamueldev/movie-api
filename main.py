from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
#Update the title of our API.
app.title = "Basic API"
#Also, we can modify its actual version.
app.version = "0.0.0.1"


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


class Item():
    name: str
    description: str | None = None

#Tags=[] help us to separate each endpoint in the documentation so we can see, verify and test each endpoint.
@app.get('/', tags=["CAsita"])
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


@app.get('/movies', tags=["Peliculas, chicles, tance"])
def get_movies():
    return movies


#Get movie by id.
@app.get('/movies/{id}', tags=["Peliculas, chicles, tance"])
#Set up id in the function parameter and specify its type
def get_movie(id: int):
    #Iterate dictionary.
    for item in movies:
        if item["id"] == id:
            return item
    return None

""" Ya se pudo :D con parametros query"""
@app.get('/name/', tags=["Peliculas, chicles, tance"])
def get_movie_by_name(nombre: str, year: str, category: str):

    categories = [cat for cat in movies if cat["categoria"] == category]
    return nombre, year, categories


@app.get('/movies/', tags=["Peliculas, chicles, tance"])
def get_movies_by_category(category: str):
    for cat in movies:
        if cat["categoria"] == category:
            return cat
    return "Ni un brillo pelao"


#POST method
@app.post('/movies', tags=["Peliculas, chicles, tance"])
def post_movie(id: int = Body(), nombre: str = Body(), año: int = Body(), categoria: str = Body(), reseña: float = Body()):
    
    movies.append({
        "id": id,
        "nombre": nombre,
        "año": año,
        "categoria": categoria,
        "reseña": reseña
    })

    return movies


#PUT method
@app.put('/movies/{id}', tags=["Peliculas, chicles, tance"])
def update_movie(id: int):
    return {"Sample text": "Updated", "id": id}