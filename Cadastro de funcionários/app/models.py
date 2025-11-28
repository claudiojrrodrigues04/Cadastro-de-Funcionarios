# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship 
from app.database import Base

# --- TABELA DE ASSOCIAÇÃO (N-M) ---
employee_project_association = Table(
    'employee_project_association',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)

# --- Tabela 1: Departamentos ---
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    employees = relationship("Employee", back_populates="department")

# --- Tabela 2: Cargos (Position) ---
class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    employees = relationship("Employee", back_populates="position")

# --- Tabela 3: Funcionários (Employee) ---
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    salary = Column(Float, nullable=True, default=0.0)
    
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    
    # Relacionamento N-M com Projetos
    projects = relationship(
        "Project",
        secondary=employee_project_association,
        back_populates="employees"
    )

# --- Tabela 4: Usuários (Autenticação) ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

# --- Tabela 5: Projetos (N-M) ---
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Relacionamento N-M com Funcionários
    employees = relationship(
        "Employee",
        secondary=employee_project_association,
        back_populates="projects"
    )