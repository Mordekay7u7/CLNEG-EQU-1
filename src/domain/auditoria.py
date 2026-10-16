"""Registro de hechos relevantes del ciclo de vida de una cita."""
from dataclasses import dataclass
from datetime import datetime
from .model import ReglaNegocioError
@dataclass(frozen=True)
class EventoAuditoria:
    entidad_id:str
    accion:str
    responsable:str
    fecha:datetime
    detalle:str
    def __post_init__(self):
        if not all([self.entidad_id.strip(),self.accion.strip(),self.responsable.strip()]):raise ReglaNegocioError("Auditoría incompleta")
class Bitacora:
    def __init__(self):self._eventos=[]
    def registrar(self,evento):self._eventos.append(evento)
    def por_entidad(self,identificador):return tuple(x for x in self._eventos if x.entidad_id==identificador)
    def por_responsable(self,responsable):return tuple(x for x in self._eventos if x.responsable==responsable)
