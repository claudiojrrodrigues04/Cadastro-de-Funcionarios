# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pathlib import Path
from contextlib import asynccontextmanager

# Importa a 'Base' e 'engine' da sua database
from app.database import Base, engine 

# Importa TODOS os routers
from app.routers import (
    employees_router, 
    departments_router, 
    positions_router,
    auth_router,        
    projects_router     
)

# --- Evento de Startup (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Isto roda ANTES do servidor ligar
    print("Servidor iniciando... Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas prontas.")
    yield
    # Isto roda DEPOIS do servidor desligar
    print("Servidor desligando...")

# Cria a instância principal do FastAPI
app = FastAPI(title="Projeto de RH", lifespan=lifespan)

# --- INCLUSÃO DE ROUTERS ---
app.include_router(auth_router)        
app.include_router(projects_router)    
app.include_router(employees_router)
app.include_router(departments_router)
app.include_router(positions_router)

# --- ARQUIVOS ESTÁTICOS ---
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")

# --- ROTAS PRINCIPAIS ---

# Rota de redirecionamento para a página de login
@app.get("/")
def home():
    # Envia o usuário para /login primeiro
    return RedirectResponse(url="/login", status_code=302) 

# Status/saúde do servidor (útil para debug)
@app.get("/status")
def status(request: Request):
    return {
        "status": "ok",
        "host": request.client.host,
        "port": request.url.port or 80,
    }