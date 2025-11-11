# app/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base # Assumindo que seu app/database.py define 'Base'


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    
    # Informações Pessoais
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Informações Profissionais
    position = Column(String(100), nullable=True) # Cargo
    department = Column(String(100), nullable=True) # Departamento
    salary = Column(Float, nullable=True, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Employee(name='{self.name}', email='{self.email}')>"