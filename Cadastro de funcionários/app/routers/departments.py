# app/routers/departments.py
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
from app.models import Department
from app.auth import get_current_user_from_cookie # <<< IMPORTAR

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/departments", tags=["Departments"])
def list_departments(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # <<< PROTEGIDO
):
    departments = db.scalars(select(Department).order_by(Department.name)).all()
    return templates.TemplateResponse(
        "departments/index.html", 
        {"request": request, "departments": departments, "user": current_user} # <<< PASSAR 'user'
    )

@router.post("/departments", tags=["Departments"])
def create_department(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie), # <<< PROTEGIDO
    name: str = Form(...)
):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Nome é obrigatório")
    
    new_dept = Department(name=name.strip())
    db.add(new_dept)
    db.commit()
    return RedirectResponse(url="/departments", status_code=status.HTTP_303_SEE_OTHER)

@router.delete("/departments/{department_id}")
def delete_department(
    department_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):
    department = db.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    # (Opcional) Aqui você poderia impedir a exclusão se tiver funcionários
    # mas vamos deixar excluir direto por enquanto.
    
    db.delete(department)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)