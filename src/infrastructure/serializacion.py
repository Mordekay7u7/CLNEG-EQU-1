"""Representación segura para vistas y reportes."""
def cita_resumen(cita):
    return {'id':cita.id,'paciente_id':cita.paciente_id,'medico_id':cita.medico_id,'sucursal_id':cita.sucursal_id,'estado':cita.estado.value,'inicio':cita.inicio.isoformat(),'fin':cita.fin.isoformat()}
