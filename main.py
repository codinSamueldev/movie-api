from fastapi import FastAPI
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
    }
]


#Tags=[] help us to separate each endpoint in the documentation so we can see, verify and test each endpoint.
@app.get('/', tags=["CAsita"])
def message():
    return "Holiiii"


@app.get('/test')
def message():
    return {"Testeo": "Si funciona"}

#Return HTML code
@app.get('/html')
def message():
    return HTMLResponse("""

    <h1>Al parecer, funciona.</h1>
    <figure>
        <div style="background: black; width: 35%; height: 51%; border-radius: 35%"></div>
    </figure> """)


@app.get('/movies', tags=["Peliculas, chicles, tance"])
def get_movies():
    return movies