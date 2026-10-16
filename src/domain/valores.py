"""Objetos de valor inmutables y validaciones temporales de MediNova."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from .model import ReglaNegocioError, solapan
@dataclass(frozen=True)
class Intervalo:
    inicio: datetime
    fin: datetime
    def __post_init__(self):
        if self.fin <= self.inicio: raise ReglaNegocioError("El fin debe ser posterior al inicio")
    @property
    def minutos(self): return int((self.fin-self.inicio).total_seconds()/60)
    def solapa(self,otro): return solapan(self.inicio,self.fin,otro.inicio,otro.fin)
    def contiene(self,otro): return self.inicio<=otro.inicio and otro.fin<=self.fin
@dataclass(frozen=True)
class Identidad:
    valor: str
    def __post_init__(self):
        if not isinstance(self.valor,str) or not self.valor.strip(): raise ReglaNegocioError("Identificador vacío")
@dataclass(frozen=True)
class PoliticaTiempo:
    retencion_minutos:int=3
    tolerancia_llegada:int=15
    ausencia_minutos:int=20
    aviso_honorarios_horas:int=24
    def __post_init__(self):
        if min(self.retencion_minutos,self.tolerancia_llegada,self.ausencia_minutos,self.aviso_honorarios_horas)<0: raise ReglaNegocioError("Duración negativa")
    def retencion_expirada(self,creada,ahora):return ahora>=creada+timedelta(minutes=self.retencion_minutos)
