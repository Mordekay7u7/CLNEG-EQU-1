"""Clasificación de estados de citas."""
from .model import EstadoCita
ACTIVAS=frozenset((EstadoCita.RESERVADA,EstadoCita.PENDIENTE_CONFIRMACION))
TERMINALES=frozenset((EstadoCita.CANCELADA,EstadoCita.ATENDIDA,EstadoCita.AUSENTE))
def activa(cita): return cita.estado in ACTIVAS
