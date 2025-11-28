# app/routers/auth.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path

# Segurança e Autenticação
from app.auth import (
    create_access_token, 
    get_password_hash, 
    verify_password
)
from app.database import get_db
from app import models

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# --- Rota 1: Página de Login (GET) ---
@router.get("/login", response_class=HTMLResponse, tags=["Auth"])
def login_form(request: Request, error: str = None, message: str = None):
    # Mostra mensagens de erro (login falhou) ou sucesso (registro OK)
    return templates.TemplateResponse(
        "auth/login.html", 
        {"request": request, "error_message": error, "success_message": message}
    )

# --- Rota 2: Processar o Login (POST) ---
# <<< CORRIGIDA >>>
@router.post("/login", tags=["Auth"])
def login_via_form_data(
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...)
    # Removemos 'response: Response' dos parâmetros
):
    user = db.scalar(select(models.User).where(models.User.username == username))
    
    if not user or not verify_password(password, user.hashed_password):
        # Falha: Redireciona de volta para /login com erro
        return RedirectResponse(
            url="/login?error=Usuário ou senha inválidos", 
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    # Sucesso: Cria o token
    access_token = create_access_token(data={"sub": user.username})
    
    # --- A CORREÇÃO ---
    # 1. Crie o objeto de resposta de redirecionamento
    redirect_response = RedirectResponse(url="/employees", status_code=status.HTTP_303_SEE_OTHER)
    
    # 2. Defina o cookie NELE
    redirect_response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True, 
        samesite="strict"
    )
    
    # 3. Retorne o objeto de redirecionamento que contém o cookie
    return redirect_response

# --- Rota 3: Página de Registro (GET) ---
@router.get("/register", response_class=HTMLResponse, tags=["Auth"])
def register_form(request: Request, error: str = None):
    return templates.TemplateResponse(
        "auth/register.html", 
        {"request": request, "error_message": error}
    )

# --- Rota 4: Processar o Registro (POST) ---
@router.post("/register", tags=["Auth"])
def register_user(
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.scalar(select(models.User).where(models.User.username == username))
    if existing_user:
        return RedirectResponse(
            url="/register?error=Nome de usuário já existe", 
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    hashed_pass = get_password_hash(password)
    new_user = models.User(username=username, hashed_password=hashed_pass)
    db.add(new_user)
    db.commit()

    # Redireciona para /login com uma mensagem de sucesso
    return RedirectResponse(url="/login?message=Conta criada com sucesso!", status_code=status.HTTP_303_SEE_OTHER)

# --- Rota 5: Logout (GET) ---
# <<< CORRIGIDA >>>
@router.get("/logout", tags=["Auth"])
def logout():
    # 1. Crie o objeto de resposta de redirecionamento
    redirect_response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # 2. Delete o cookie NELE
    redirect_response.delete_cookie("access_token")
    
    # 3. Retorne a resposta
    return redirect_response