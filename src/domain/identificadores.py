"""Identificadores de negocio."""
from .model import ReglaNegocioError
def obligatorio(valor, etiqueta):
    if not isinstance(valor,str) or not valor.strip(): raise ReglaNegocioError(f'{etiqueta} obligatorio')
    return valor.strip()
