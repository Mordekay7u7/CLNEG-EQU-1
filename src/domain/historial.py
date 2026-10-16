"""Consultas de historial sin acceso a infraestructura."""
from collections import Counter
from .model import EstadoCita
def resumen_paciente(citas,paciente_id):
    elegidas=[c for c in citas if c.paciente_id==paciente_id]
    conteo=Counter(c.estado.value for c in elegidas)
    return {'paciente_id':paciente_id,'total':len(elegidas),'reservadas':conteo[EstadoCita.RESERVADA.value],
            'canceladas':conteo[EstadoCita.CANCELADA.value],'atendidas':conteo[EstadoCita.ATENDIDA.value],
            'ausentes':conteo[EstadoCita.AUSENTE.value],'pendientes_confirmacion':conteo[EstadoCita.PENDIENTE_CONFIRMACION.value]}
