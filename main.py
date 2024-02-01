from routers import movies, jwt_manager_auth, html_endpoints, users
from fastapi import FastAPI
from config.database import engine, Base
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

#Tags=[] help us to separate each endpoint in the documentation so we can see, verify and test each endpoint.
@app.get('/', tags=["Casita"])
def message():
    return "Holiiii"

