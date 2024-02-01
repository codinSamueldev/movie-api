from fastapi import APIRouter
from fastapi.responses import HTMLResponse

html_router = APIRouter(prefix="/html",
                        tags=["HTML test"])


#Return HTML code
@html_router.get("")
def message():
    return HTMLResponse("""

    <h1>Al parecer, funciona.</h1>
    <figure>
        <div style="background: black; width: 35%; height: 51%; border-radius: 35%"></div>
    </figure> """)
