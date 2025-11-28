# app/routers/projects.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from pathlib import Path

from app.database import get_db
from app import models
from app.auth import get_current_user_from_cookie # Importar para proteger

# Protege TODAS as rotas neste arquivo
router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user_from_cookie)]
)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# --- 1. Listar Projetos (Read) ---
@router.get("/")
def list_projects(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # Dependência duplicada é ok
):
    projects = db.scalars(
        select(models.Project).options(joinedload(models.Project.employees))
    ).unique().all()
    
    return templates.TemplateResponse(
        "projects/index.html", 
        {"request": request, "projects": projects, "user": current_user}
    )

# --- 2. Criar Projeto (Create) ---
@router.post("/")
def create_project(name: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    new_project = models.Project(name=name, description=description)
    db.add(new_project)
    db.commit()
    return RedirectResponse(url="/projects", status_code=status.HTTP_303_SEE_OTHER)

# --- 3. Detalhes do Projeto (Read N-M) ---
@router.get("/{project_id}")
def project_details(
    project_id: int, 
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):
    project = db.scalar(
        select(models.Project)
        .where(models.Project.id == project_id)
        .options(joinedload(models.Project.employees))
    )
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    all_employees = db.scalars(select(models.Employee).order_by(models.Employee.name)).all()

    return templates.TemplateResponse(
        "projects/show.html",
        {
            "request": request,
            "project": project,
            "all_employees": all_employees,
            "user": current_user
        }
    )

# --- 4. Adicionar Funcionário a um Projeto (Update N-M) ---
@router.post("/{project_id}/add_employee")
def add_employee_to_project(
    project_id: int, 
    employee_id: int = Form(...), 
    db: Session = Depends(get_db)
):
    project = db.get(models.Project, project_id)
    employee = db.get(models.Employee, employee_id)

    if employee not in project.employees:
        project.employees.append(employee)
        db.commit()

    return RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)

# --- 5. Remover Funcionário de um Projeto (Update N-M) ---
@router.post("/{project_id}/remove_employee/{employee_id}")
def remove_employee_from_project(
    project_id: int, 
    employee_id: int, 
    db: Session = Depends(get_db)
):
    project = db.get(models.Project, project_id)
    employee = db.get(models.Employee, employee_id)

    if employee in project.employees:
        project.employees.remove(employee)
        db.commit()

    return RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)