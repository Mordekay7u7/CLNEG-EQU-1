"""Capacidad disponible por jornada."""
from .model import EstadoCita
def ocupacion(jornada,citas):
    return sum(c.medico_id==jornada.medico_id and c.sucursal_id==jornada.sucursal_id and c.estado==EstadoCita.RESERVADA and jornada.inicio<=c.inicio<jornada.fin for c in citas)
def lugares_disponibles(jornada,citas): return max(0,jornada.capacidad-ocupacion(jornada,citas))
