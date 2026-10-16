"""Composición de servicios con dependencias en memoria."""
from application.services import ServicioCitas
from .memory import RepositorioCitasMemoria
def crear_servicio(jornadas=None): return ServicioCitas(RepositorioCitasMemoria(),list(jornadas or []),[])
