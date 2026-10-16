"""Entidades y reglas de negocio de MediNova. Sin dependencias externas."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class ReglaNegocioError(ValueError): pass
class EstadoCita(str, Enum):
    RESERVADA='reservada'; CANCELADA='cancelada'; ATENDIDA='atendida'; AUSENTE='ausente'; PENDIENTE_CONFIRMACION='pendiente_confirmacion'

@dataclass
class Cita:
    id: str
    paciente_id: str
    medico_id: str
    sucursal_id: str
    inicio: datetime
    fin: datetime
    estado: EstadoCita = EstadoCita.RESERVADA
    motivo_cancelacion: str = ''
    cancelada_por: str = ''
    cancelada_en: datetime | None = None
    llegada: datetime | None = None
    validacion_medico: bool = False
    def __post_init__(self):
        if not all((self.id,self.paciente_id,self.medico_id,self.sucursal_id)): raise ReglaNegocioError('Identificadores obligatorios')
        if self.fin <= self.inicio: raise ReglaNegocioError('Horario inválido')
    def cancelar(self,motivo,actor,ahora):
        if self.estado != EstadoCita.RESERVADA: raise ReglaNegocioError('Solo citas reservadas')
        if not motivo.strip() or not actor.strip(): raise ReglaNegocioError('Motivo y responsable obligatorios')
        self.estado=EstadoCita.CANCELADA; self.motivo_cancelacion=motivo.strip();self.cancelada_por=actor.strip();self.cancelada_en=ahora
    def registrar_llegada(self,ahora,autorizada=False):
        if self.estado != EstadoCita.RESERVADA: raise ReglaNegocioError('Cita no activa')
        if ahora > self.inicio + timedelta(minutes=15) and not autorizada: raise ReglaNegocioError('Requiere autorización médica')
        self.llegada=ahora;self.validacion_medico=autorizada
    def registrar_ausencia(self,ahora):
        if self.estado != EstadoCita.RESERVADA or self.llegada is not None: raise ReglaNegocioError('No corresponde ausencia')
        if ahora < self.inicio + timedelta(minutes=20): raise ReglaNegocioError('Esperar 20 minutos')
        self.estado=EstadoCita.AUSENTE
    def atender(self):
        if self.estado != EstadoCita.RESERVADA or self.llegada is None: raise ReglaNegocioError('Debe registrar llegada')
        self.estado=EstadoCita.ATENDIDA

@dataclass
class JornadaMedica:
    id: str
    medico_id: str
    sucursal_id: str
    inicio: datetime
    fin: datetime
    capacidad: int
    sobrecupos: int = 0
    cancelada: bool = False
    def __post_init__(self):
        if self.fin <= self.inicio or self.capacidad <= 0: raise ReglaNegocioError('Jornada inválida')
    def contiene(self,cita):
        return cita.medico_id==self.medico_id and cita.sucursal_id==self.sucursal_id and self.inicio<=cita.inicio and cita.fin<=self.fin and not self.cancelada
    def permitir_sobrecupo(self,autorizacion_medica):
        if not autorizacion_medica or self.sobrecupos>=2: raise ReglaNegocioError('Sobrecupo requiere autorización y máximo dos')
        self.sobrecupos+=1
    def cancelar(self,tipo_contrato,ahora,justificante=False):
        if tipo_contrato=='empleado' and not justificante: raise ReglaNegocioError('Se requiere justificante')
        if tipo_contrato=='honorarios' and self.inicio-ahora < timedelta(hours=24): raise ReglaNegocioError('Aviso mínimo 24 horas')
        if tipo_contrato not in ('empleado','honorarios'): raise ReglaNegocioError('Contrato desconocido')
        self.cancelada=True

@dataclass
class Retencion:
    paciente_id: str
    medico_id: str
    inicio: datetime
    fin: datetime
    creada_en: datetime
    @property
    def vence_en(self): return self.creada_en + timedelta(minutes=3)
    def vigente(self,ahora): return ahora < self.vence_en

def solapan(a_inicio,a_fin,b_inicio,b_fin): return a_inicio < b_fin and b_inicio < a_fin

def restringido_por_ausencias(citas,paciente_id,ahora):
    limite=ahora-timedelta(days=183)
    return sum(c.paciente_id==paciente_id and c.estado==EstadoCita.AUSENTE and limite<=c.inicio<=ahora for c in citas)>=3
