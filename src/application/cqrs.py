"""Separación de comandos de escritura y consultas de lectura."""
from domain.model import Cita
from domain.historial import resumen_paciente
class ComandosCitas:
    def __init__(self,servicio):self.servicio=servicio
    def reservar(self,cmd,ahora):
        cita=Cita(cmd.id,cmd.paciente_id,cmd.medico_id,cmd.sucursal_id,cmd.inicio,cmd.fin)
        return self.servicio.reservar(cita,ahora,cmd.canal,cmd.anticipo_presencial,cmd.autorizacion_sobrecupo)
    def cancelar(self,cmd):return self.servicio.cancelar(cmd.cita_id,cmd.motivo,cmd.responsable,cmd.fecha)
    def llegada(self,cmd):return self.servicio.llegada(cmd.cita_id,cmd.fecha,cmd.autorizacion_medica)
class ConsultasCitas:
    def __init__(self,repositorio):self.repositorio=repositorio
    def paciente(self,id):return tuple(c for c in self.repositorio.listar() if c.paciente_id==id)
    def medico(self,id):return tuple(c for c in self.repositorio.listar() if c.medico_id==id)
    def historial(self,id):return resumen_paciente(self.repositorio.listar(),id)
    def por_estado(self,estado):return tuple(c for c in self.repositorio.listar() if c.estado==estado)
