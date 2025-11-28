# app/routers/positions.py
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path
from app.database import get_db
from app import models # Importar models
from app.models import Position
from app.auth import get_current_user_from_cookie # <<< IMPORTAR

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/positions", tags=["Positions"])
def list_positions(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # <<< PROTEGIDO
):
    positions = db.scalars(select(Position).order_by(Position.title)).all()
    return templates.TemplateResponse(
        "positions/index.html", 
        {"request": request, "positions": positions, "user": current_user} # <<< PASSAR 'user'
    )

@router.post("/positions", tags=["Positions"])
def create_position(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie), # <<< PROTEGIDO
    title: str = Form(...)
):
    if not title.strip():
        raise HTTPException(status_code=400, detail="Título é obrigatório")
    
    new_pos = Position(title=title.strip())
    db.add(new_pos)
    db.commit()
    return RedirectResponse(url="/positions", status_code=status.HTTP_303_SEE_OTHER)

@router.delete("/positions/{position_id}")
def delete_position(
    position_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):
    # Busca o cargo pelo ID
    position = db.get(Position, position_id)
    
    if not position:
        raise HTTPException(status_code=404, detail="Cargo não encontrado")

    # Deleta do banco
    db.delete(position)
    db.commit()
    
    # Retorna sucesso sem conteúdo (204)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)