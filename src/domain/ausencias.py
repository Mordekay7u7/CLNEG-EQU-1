"""Historial de inasistencias."""
from datetime import timedelta
from .model import EstadoCita
def contar(citas,paciente,ahora,dias=183):
    limite=ahora-timedelta(days=dias)
    return sum(c.paciente_id==paciente and c.estado==EstadoCita.AUSENTE and limite<=c.inicio<=ahora for c in citas)
def requiere_anticipo(citas,paciente,ahora): return contar(citas,paciente,ahora)>=3
