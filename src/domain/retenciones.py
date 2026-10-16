"""Política de vigencia y exclusión de retenciones."""
from .model import solapan
def bloqueada(retenciones,medico,inicio,fin,ahora,paciente=None):
    return any(r.vigente(ahora) and r.medico_id==medico and (paciente is None or r.paciente_id!=paciente) and solapan(inicio,fin,r.inicio,r.fin) for r in retenciones)
def depurar(retenciones,ahora): return [r for r in retenciones if r.vigente(ahora)]
