# app/routers/employees.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from pathlib import Path
from app.database import get_db
from app import models # Importar 'models' para o 'current_user'
from app.models import Employee, Department, Position 
from app.helpers import format_brl_price, format_brl_date
# <<< 1. IMPORTAR A NOVA DEPENDÊNCIA >>>
from app.auth import get_current_user_from_cookie

router = APIRouter()
# <<< LINHA 'Base.metadata.create_all' REMOVIDA DAQUI >>>

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["brl_price"] = format_brl_price
templates.env.filters["brl_date"] = format_brl_date

@router.get("/", include_in_schema=False)
def root_redirect():
    # Esta rota pode ser pública, ela só redireciona
    return RedirectResponse(url="/employees", status_code=status.HTTP_302_FOUND)

# --- LISTAR FUNCIONÁRIOS (PROTEGIDO) ---
@router.get("/employees")
def list_employees(
    request: Request, 
    db: Session = Depends(get_db),
    # <<< 2. ADICIONAR DEPENDÊNCIA DE AUTENTICAÇÃO >>>
    current_user: models.User = Depends(get_current_user_from_cookie)
):
    query = (
        select(Employee)
        .options(
            joinedload(Employee.department), 
            joinedload(Employee.position)
        )
        .order_by(Employee.id.desc())
    )
    employees = db.scalars(query).all()
    
    return templates.TemplateResponse(
        "employees/index.html", 
        # <<< 3. PASSAR 'user' PARA O TEMPLATE (para o cabeçalho) >>>
        {"request": request, "employees": employees, "user": current_user}
    )

# --- FORMULÁRIO DE NOVO FUNCIONÁRIO (PROTEGIDO) ---
@router.get("/employees/new")
def new_employee_form(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # <<< PROTEGIDO
): 
    departments = db.scalars(select(Department).order_by(Department.name)).all()
    positions = db.scalars(select(Position).order_by(Position.title)).all()
    
    return templates.TemplateResponse(
        "employees/new.html", 
        {
            "request": request,
            "action": "/employees",
            "method_override": "POST",
            "employee": None,
            "departments": departments, 
            "positions": positions,
            "user": current_user # <<< PASSAR 'user'
        }
    )

# --- FORMULÁRIO DE EDIÇÃO (PROTEGIDO) ---
@router.get("/employees/{employee_id}/edit")
def edit_employee_form(
    employee_id: int, 
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # <<< PROTEGIDO
):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    departments = db.scalars(select(Department).order_by(Department.name)).all()
    positions = db.scalars(select(Position).order_by(Position.title)).all()

    return templates.TemplateResponse(
        "employees/edit.html", 
        {
            "request": request,
            "action": f"/employees/{employee.id}",
            "method_override": "PUT",
            "employee": employee,
            "departments": departments,
            "positions": positions,
            "user": current_user # <<< PASSAR 'user'
        }
    )

# --- CRIAÇÃO DE FUNCIONÁRIO (PROTEGIDO) ---
@router.post("/employees")
def create_employee(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie), # <<< PROTEGIDO
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    salary: float = Form(0.0),
    department_id: int = Form(None),
    position_id: int = Form(None)
):
    # ... (lógica da rota permanece a mesma) ...
    db.add(Employee(
        name=name.strip(), 
        email=email.strip(),
        phone=phone.strip() if phone else None,
        salary=salary,
        department_id=department_id,
        position_id=position_id
    ))
    db.commit()
    return RedirectResponse(url="/employees", status_code=status.HTTP_303_SEE_OTHER)

# --- ATUALIZAÇÃO DE FUNCIONÁRIO (PROTEGIDO) ---
@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie), # <<< PROTEGIDO
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    salary: float = Form(0.0),
    department_id: int = Form(None),
    position_id: int = Form(None)
):
    # ... (lógica da rota permanece a mesma) ...
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    employee.name = name.strip()
    employee.email = email.strip()
    employee.phone = phone.strip() if phone else None
    employee.salary = salary
    employee.department_id = department_id
    employee.position_id = position_id
    db.add(employee)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

# --- EXCLUSÃO DE FUNCIONÁRIO (PROTEGIDO) ---
@router.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # <<< PROTEGIDO
):
    # ... (lógica da rota permanece a mesma) ...
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    db.delete(employee)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

# --- DETALHE DE FUNCIONÁRIO (PROTEGIDO) ---
@router.get("/employees/{employee_id}")
def get_employee(
    employee_id: int, 
    request: Request, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie) # <<< PROTEGIDO
):
    query = (
        select(Employee)
        .where(Employee.id == employee_id)
        .options(
            joinedload(Employee.department),
            joinedload(Employee.position)
        )
    )
    employee = db.scalar(query) 

    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return templates.TemplateResponse(
        "employees/show.html", 
        {"request": request, "employee": employee, "user": current_user} # <<< PASSAR 'user'
    )