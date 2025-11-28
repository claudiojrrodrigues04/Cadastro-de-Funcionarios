# app/auth.py
from fastapi import Depends, HTTPException, status, Request # <<< Request FOI ADICIONADO
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from app import models 
from app.database import get_db

# --- Configuração de Segurança ---

# 1. Contexto do Passlib (para Hashing de Senha)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configs do JWT (Token)
SECRET_KEY = "SUA_CHAVE_SECRETA_MUITO_FORTE" # <-- TROQUE ISSO
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Funções Auxiliares de Segurança ---

def verify_password(plain_password, hashed_password):
    """Verifica se a senha plana bate com o hash salvo"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Gera um hash de uma senha plana"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Cria um token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- <<< NOVA DEPENDÊNCIA (O "OUTRO JEITO") >>> ---

def get_current_user_from_cookie(
    request: Request, # Precisamos do 'request' para ler os cookies
    db: Session = Depends(get_db)
) -> models.User:
    """
    Decodifica o token do cookie, valida o usuário e retorna o objeto User.
    Esta é a nova dependência que "protege" as rotas.
    """
    
    # 1. Tenta pegar o token do cookie
    token = request.cookies.get("access_token")

    # 2. Define a exceção de "Não Logado"
    credentials_exception = HTTPException(
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
        detail="Não autenticado",
        headers={"Location": "/login"}, # Joga o usuário para /login
    )

    if token is None:
        raise credentials_exception
    
    # 3. Limpa o prefixo "Bearer " do token
    try:
        token_prefix, token_value = token.split(" ")
        if token_prefix.lower() != "bearer":
            raise credentials_exception
    except ValueError:
        raise credentials_exception
    
    # 4. Decodifica o JWT
    try:
        payload = jwt.decode(token_value, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 5. Busca o usuário no banco de dados
    user = db.scalar(select(models.User).where(models.User.username == username))
    if user is None:
        raise credentials_exception
    
    # 6. Sucesso! Retorna o usuário
    return user