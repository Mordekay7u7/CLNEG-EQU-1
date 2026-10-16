import unittest
from datetime import datetime,timedelta
from domain.model import Cita,EstadoCita,ReglaNegocioError
from domain.valores import Intervalo,Identidad,PoliticaTiempo
from domain.politicas import validar_agenda_paciente,validar_agenda_medico,validar_canal
from domain.auditoria import Bitacora,EventoAuditoria
from domain.historial import resumen_paciente
from application.cqrs import ConsultasCitas,ComandosCitas
from application.comandos import SolicitarReserva,SolicitarCancelacion,RegistrarLlegada
from application.indicadores import indicadores_citas
from infrastructure.memory import RepositorioCitasMemoria as RepositorioMemoria
from infrastructure.adaptadores import NotificadorMemoria,RelojFijo
from infrastructure.unidad_trabajo import UnidadTrabajoMemoria
from application.services import ServicioCitas
from domain.model import JornadaMedica
T=datetime(2026,10,20,9)
def cita(n='1',pac='P1',med='M1',hora=9):return Cita(n,pac,med,'S1',T.replace(hour=hora),T.replace(hour=hora)+timedelta(minutes=30))
class ValoresTest(unittest.TestCase):
 def test_intervalo_valido(self):self.assertEqual(Intervalo(T,T+timedelta(minutes=30)).minutos,30)
 def test_intervalo_invalido(self):
  with self.assertRaises(ReglaNegocioError):Intervalo(T,T)
 def test_intervalo_solapa(self):self.assertTrue(Intervalo(T,T+timedelta(minutes=30)).solapa(Intervalo(T+timedelta(minutes=20),T+timedelta(minutes=40))))
 def test_intervalo_contiene(self):self.assertTrue(Intervalo(T,T+timedelta(hours=1)).contiene(Intervalo(T,T+timedelta(minutes=30))))
 def test_identidad_valida(self):self.assertEqual(Identidad('P1').valor,'P1')
 def test_identidad_vacia(self):
  with self.assertRaises(ReglaNegocioError):Identidad(' ')
 def test_politica_limite(self):self.assertTrue(PoliticaTiempo().retencion_expirada(T,T+timedelta(minutes=3)))
 def test_politica_no_expirada(self):self.assertFalse(PoliticaTiempo().retencion_expirada(T,T+timedelta(minutes=2)))
 def test_politica_negativa(self):
  with self.assertRaises(ReglaNegocioError):PoliticaTiempo(retencion_minutos=-1)
class PoliticasTest(unittest.TestCase):
 def test_paciente_mismo_horario(self):
  with self.assertRaises(ReglaNegocioError):validar_agenda_paciente(cita('2','P1','M2'),[cita()])
 def test_paciente_diferente(self):validar_agenda_paciente(cita('2','P2','M2'),[cita()])
 def test_medico_ocupado(self):
  with self.assertRaises(ReglaNegocioError):validar_agenda_medico(cita('2','P2'),[cita()])
 def test_medico_libre(self):validar_agenda_medico(cita('2','P2','M2'),[cita()])
 def test_canal_invalido(self):
  with self.assertRaises(ReglaNegocioError):validar_canal([],'P1',T,'desconocido',False)
 def test_canal_recepcion(self):validar_canal([],'P1',T,'recepcion',False)
class AuditoriaTest(unittest.TestCase):
 def test_registro(self):
  b=Bitacora();b.registrar(EventoAuditoria('C1','cancelar','recepcion',T,'motivo'));self.assertEqual(len(b.por_entidad('C1')),1)
 def test_por_responsable(self):
  b=Bitacora();b.registrar(EventoAuditoria('C1','cancelar','recepcion',T,'motivo'));self.assertEqual(len(b.por_responsable('recepcion')),1)
 def test_evento_invalido(self):
  with self.assertRaises(ReglaNegocioError):EventoAuditoria('','cancelar','recepcion',T,'motivo')
class ConsultasTest(unittest.TestCase):
 def setUp(self):self.repo=RepositorioMemoria();self.repo.guardar(cita());self.repo.guardar(cita('2','P2','M2',10));self.cons=ConsultasCitas(self.repo)
 def test_por_paciente(self):self.assertEqual(len(self.cons.paciente('P1')),1)
 def test_por_medico(self):self.assertEqual(len(self.cons.medico('M2')),1)
 def test_por_estado(self):self.assertEqual(len(self.cons.por_estado(EstadoCita.RESERVADA)),2)
 def test_historial(self):self.assertEqual(self.cons.historial('P1')['total'],1)
 def test_historial_vacio(self):self.assertEqual(resumen_paciente([],'P1')['total'],0)
 def test_indicadores(self):self.assertEqual(indicadores_citas(self.repo.listar())['total'],2)
 def test_indicadores_vacios(self):self.assertEqual(indicadores_citas([])['porcentaje_ausencias'],0)
class AdaptadoresTest(unittest.TestCase):
 def test_notificador(self):self.assertEqual(len(NotificadorMemoria().enviadas),0)
 def test_envio(self):
  n=NotificadorMemoria();n.enviar('P1','Cita','Aviso');self.assertEqual(len(n.enviadas),1)
 def test_envio_invalido(self):
  with self.assertRaises(ValueError):NotificadorMemoria().enviar('','Cita','Aviso')
 def test_reloj(self):
  r=RelojFijo(T);r.avanzar(timedelta(minutes=1));self.assertEqual(r.ahora(),T+timedelta(minutes=1))
 def test_rollback(self):
  r=RepositorioMemoria()
  with UnidadTrabajoMemoria(r):r.guardar(cita())
  self.assertEqual(len(r.listar()),0)
 def test_commit(self):
  r=RepositorioMemoria()
  with UnidadTrabajoMemoria(r) as u:r.guardar(cita());u.confirmar()
  self.assertEqual(len(r.listar()),1)
 def test_excepcion_revierte(self):
  r=RepositorioMemoria()
  with self.assertRaises(RuntimeError):
   with UnidadTrabajoMemoria(r) as u:r.guardar(cita());u.confirmar();raise RuntimeError('error')
  self.assertEqual(len(r.listar()),0)
class ComandosTest(unittest.TestCase):
 def setUp(self):
  self.r=RepositorioMemoria();j=JornadaMedica('J','M1','S1',T,T+timedelta(hours=8),8);self.s=ServicioCitas(self.r,[j],[]);self.c=ComandosCitas(self.s)
 def test_reservar(self):
  cmd=SolicitarReserva('C','P','M1','S1',T,T+timedelta(minutes=30));self.c.reservar(cmd,T-timedelta(days=1));self.assertEqual(len(self.r.listar()),1)
 def test_cancelar(self):
  self.r.guardar(cita());self.c.cancelar(SolicitarCancelacion('1','Paciente solicita','recepcion',T));self.assertEqual(self.r.obtener('1').estado,EstadoCita.CANCELADA)
 def test_llegada(self):
  self.r.guardar(cita());self.c.llegada(RegistrarLlegada('1',T));self.assertEqual(self.r.obtener('1').llegada,T)
