"""Casos de uso: orquestación, sin reglas duplicadas de dominio."""
from datetime import datetime
from domain.model import Cita, Retencion, EstadoCita, ReglaNegocioError, solapan, restringido_por_ausencias

class ServicioCitas:
    def __init__(self, repositorio, jornadas, retenciones):
        self.repo=repositorio;self.jornadas=jornadas;self.retenciones=retenciones
    def retener(self,paciente,medico,inicio,fin,ahora):
        if fin<=inicio: raise ReglaNegocioError('Horario inválido')
        for r in self.retenciones:
            if r.vigente(ahora) and r.medico_id==medico and solapan(inicio,fin,r.inicio,r.fin):
                raise ReglaNegocioError('Franja temporalmente retenida')
        r=Retencion(paciente,medico,inicio,fin,ahora);self.retenciones.append(r);return r
    def reservar(self,cita,ahora,canal='recepcion',anticipo_presencial=False,autorizacion_sobrecupo=False):
        if self.repo.obtener(cita.id): raise ReglaNegocioError('ID repetido')
        todas=self.repo.listar()
        if canal=='remoto' and restringido_por_ausencias(todas,cita.paciente_id,ahora) and not anticipo_presencial:
            raise ReglaNegocioError('Requiere anticipo presencial')
        for anterior in todas:
            if anterior.estado in (EstadoCita.RESERVADA,EstadoCita.PENDIENTE_CONFIRMACION):
                if anterior.paciente_id==cita.paciente_id and solapan(cita.inicio,cita.fin,anterior.inicio,anterior.fin):
                    raise ReglaNegocioError('Paciente con cita simultánea')
                if anterior.medico_id==cita.medico_id and solapan(cita.inicio,cita.fin,anterior.inicio,anterior.fin):
                    raise ReglaNegocioError('Médico ocupado')
        for r in self.retenciones:
            if r.vigente(ahora) and r.medico_id==cita.medico_id and r.paciente_id!=cita.paciente_id and solapan(cita.inicio,cita.fin,r.inicio,r.fin):
                raise ReglaNegocioError('Horario retenido')
        jornada=next((j for j in self.jornadas if j.contiene(cita)),None)
        if not jornada: raise ReglaNegocioError('Fuera de jornada')
        ocupacion=sum(x.medico_id==cita.medico_id and x.estado==EstadoCita.RESERVADA and jornada.inicio<=x.inicio<jornada.fin for x in todas)
        if ocupacion>=jornada.capacidad:
            jornada.permitir_sobrecupo(autorizacion_sobrecupo)
        self.repo.guardar(cita)
        return cita
    def cancelar(self,id,motivo,actor,ahora):
        cita=self._obtener(id);cita.cancelar(motivo,actor,ahora);self.repo.guardar(cita);return cita
    def llegada(self,id,ahora,autorizada=False):
        cita=self._obtener(id);cita.registrar_llegada(ahora,autorizada);self.repo.guardar(cita);return cita
    def ausencia(self,id,ahora):
        cita=self._obtener(id);cita.registrar_ausencia(ahora);self.repo.guardar(cita);return cita
    def atender(self,id):
        cita=self._obtener(id);cita.atender();self.repo.guardar(cita);return cita
    def consultar_paciente(self,id): return [c for c in self.repo.listar() if c.paciente_id==id]
    def cancelar_jornada(self,jornada,tipo,ahora,justificante=False):
        jornada.cancelar(tipo,ahora,justificante)
        for c in self.repo.listar():
            if c.estado==EstadoCita.RESERVADA and c.medico_id==jornada.medico_id and jornada.inicio<=c.inicio<jornada.fin:
                c.estado=EstadoCita.PENDIENTE_CONFIRMACION;self.repo.guardar(c)
    def _obtener(self,id):
        cita=self.repo.obtener(id)
        if cita is None: raise ReglaNegocioError('Cita inexistente')
        return cita
