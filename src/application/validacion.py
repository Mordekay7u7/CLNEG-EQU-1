"""Validación de parámetros de entrada."""
from domain.model import ReglaNegocioError
def canal_valido(canal):
    if canal not in ('recepcion','remoto','telefono','whatsapp'): raise ReglaNegocioError('Canal no permitido')
    return canal
