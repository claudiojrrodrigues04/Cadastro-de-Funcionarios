# app/routers/__init__.py

# Importe os 'routers' de cada arquivo
from .employees import router as employees_router
from .departments import router as departments_router
from .positions import router as positions_router
# --- NOVAS IMPORTAÇÕES ---
from .auth import router as auth_router
from .projects import router as projects_router


# "Exporte" os routers para que o main.py possa encontrá-los
__all__ = [
    "employees_router",
    "departments_router",
    "positions_router",
    # --- NOVAS EXPORTAÇÕES ---
    "auth_router",
    "projects_router",
]