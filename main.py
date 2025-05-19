from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
#from core.config import settings

#inicializamos la app
app = FastAPI(
    # title=settings.proyect_name,
    # description=settings.description,
    # version=settings.version
    )

@app.get("/")
def read_root():
    return {"mensaje": "Hola, mundo con FastAPI"}