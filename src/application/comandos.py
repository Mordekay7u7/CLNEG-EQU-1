"""Datos de entrada explícitos para casos de uso de la capa de aplicación."""
from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class SolicitarReserva:
    id:str; paciente_id:str; medico_id:str; sucursal_id:str; inicio:datetime; fin:datetime
    canal:str='recepcion'; anticipo_presencial:bool=False; autorizacion_sobrecupo:bool=False
@dataclass(frozen=True)
class SolicitarCancelacion:
    cita_id:str; motivo:str; responsable:str; fecha:datetime
@dataclass(frozen=True)
class RegistrarLlegada:
    cita_id:str; fecha:datetime; autorizacion_medica:bool=False
