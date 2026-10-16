"""Políticas reutilizables: conflictos, ausencias y confirmación."""
from .model import EstadoCita, ReglaNegocioError, solapan, restringido_por_ausencias
ACTIVAS=frozenset([EstadoCita.RESERVADA,EstadoCita.PENDIENTE_CONFIRMACION])
def validar_agenda_paciente(cita,existentes):
    for otra in existentes:
        if otra.id!=cita.id and otra.paciente_id==cita.paciente_id and otra.estado in ACTIVAS and solapan(cita.inicio,cita.fin,otra.inicio,otra.fin):
            raise ReglaNegocioError("Paciente ya tiene cita activa en ese horario")
def validar_agenda_medico(cita,existentes):
    for otra in existentes:
        if otra.id!=cita.id and otra.medico_id==cita.medico_id and otra.estado in ACTIVAS and solapan(cita.inicio,cita.fin,otra.inicio,otra.fin):
            raise ReglaNegocioError("Médico ya tiene cita activa en ese horario")
def validar_canal(citas,paciente,ahora,canal,anticipo_presencial):
    if canal not in ('remoto','recepcion','presencial'):raise ReglaNegocioError("Canal no reconocido")
    if canal=='remoto' and restringido_por_ausencias(citas,paciente,ahora) and not anticipo_presencial:
        raise ReglaNegocioError("Se requiere anticipo presencial")
