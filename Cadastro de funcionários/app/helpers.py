# app/helpers.py
from datetime import datetime

def format_brl_price(value: float | int | None) -> str:
    """
    Formata um número para o padrão R$ 1.234,50
    """
    if value is None:
        value = 0.0
    try:
        # Formata com separador de milhar (,) e 2 casas decimais (.)
        formatted_str = f"{value:,.2f}"
        
        # Troca , por v (temp)
        formatted_str = formatted_str.replace(",", "v")
        # Troca . por , (decimal)
        formatted_str = formatted_str.replace(".", ",")
        # Troca v (temp) por . (milhar)
        formatted_str = formatted_str.replace("v", ".")
        
        return f"R$ {formatted_str}"
    except (ValueError, TypeError):
        return "R$ 0,00"

def format_brl_date(value: datetime | None) -> str:
    """
    Formata um objeto datetime para DD/MM/AAAA HH:MM
    """
    if value is None:
        return "N/A"
    try:
        return value.strftime("%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return str(value)

def parse_brl_price(value: str | int | float | None) -> float:
    """
    Converte uma string (R$ 1.234,50 ou 1234.50) para um float (1234.50)
    """
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    
    try:
        # Remove "R$", espaços e pontos de milhar
        s = str(value).strip().replace("R$", "").replace(".", "")
        # Substitui vírgula decimal por ponto
        s = s.replace(",", ".")
        
        return float(s)
    except (ValueError, TypeError):
        return 0.0