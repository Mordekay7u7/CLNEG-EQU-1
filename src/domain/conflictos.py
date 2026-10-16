"""Detección de cruces entre agendas."""
from .model import solapan
from .estados import activa
def conflictos_paciente(cita,citas):
    return [x for x in citas if x.id!=cita.id and activa(x) and x.paciente_id==cita.paciente_id and solapan(x.inicio,x.fin,cita.inicio,cita.fin)]
def conflictos_medico(cita,citas):
    return [x for x in citas if x.id!=cita.id and activa(x) and x.medico_id==cita.medico_id and solapan(x.inicio,x.fin,cita.inicio,cita.fin)]
