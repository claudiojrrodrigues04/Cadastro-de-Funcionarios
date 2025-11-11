# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o caminho do arquivo de banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Cria o "motor" do banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Necessário para SQLite
)

# Cria uma "fábrica" de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos (como o Employee)
Base = declarative_base()

# Função 'helper' para obter uma sessão no banco em cada rota
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()