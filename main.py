from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def message():
    return "Holiiii"

@app.get('/test')
def message():
    return "Probandooo"