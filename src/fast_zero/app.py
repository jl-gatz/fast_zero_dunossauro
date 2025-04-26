from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root() -> dict:
    return {'message': 'Olá, mundo!!'}


@app.get('/pagina', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_root_html() -> HTMLResponse:
    return """
    <html>
        <head>
            <title>Olá, crododilo!! 🐊</title>
        </head>
        <body>
            <h1>Olá, crocodilo!! 🐊</h1>
            <h3>by ehNoisNaFita</h3>
        </body>
    </html>
    """
