# main.py

from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from pathlib import Path

# Importa o roteador de funcionários
from app.routers import employees 

# Define o diretório base do projeto (onde o main.py está)
BASE_DIR = Path(__file__).resolve().parent

# CORREÇÃO 1: Inicializa o Jinja2Templates
# Aponta para a pasta 'app/templates'
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

app = FastAPI()

# Inclui o roteador
app.include_router(employees.router)

# Rota de redirecionamento para o index de funcionários
@app.get("/")
def home():
    return RedirectResponse(url="/employees")

# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

# #############################################################
# 1. Esta linha DEVE apontar para 'employees'
from app.routers.employees import router as employees_router 
# #############################################################

app = FastAPI(title="Projeto")

# #############################################################
# 2. Esta linha DEVE ser o 'employees_router'
app.include_router(employees_router) 
# #############################################################


# #############################################################
# 3. Esta linha é a MAIS IMPORTANTE para corrigir o erro 404.
#    Verifique se 'directory="app/static"' está IDÊNTICO.
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# #############################################################


# Status/saúde do servidor (com host/porta)
@app.get("/status")
def status(request: Request):
    return {
        "status": "ok",
        "host": request.client.host,
        "port": request.url.port or 80,
        "scheme": request.url.scheme,
        "path": request.url.path,
    }