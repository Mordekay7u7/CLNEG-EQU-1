"""Operaciones puras sobre franjas horarias."""
from dataclasses import dataclass
from datetime import datetime
from .model import ReglaNegocioError,solapan
@dataclass(frozen=True)
class Intervalo:
    inicio: datetime
    fin: datetime
    def __post_init__(self):
        if self.fin<=self.inicio: raise ReglaNegocioError('Intervalo inválido')
    def coincide(self,otro): return solapan(self.inicio,self.fin,otro.inicio,otro.fin)
    def contiene(self,otro): return self.inicio<=otro.inicio and otro.fin<=self.fin
    @property
    def minutos(self): return (self.fin-self.inicio).total_seconds()/60
