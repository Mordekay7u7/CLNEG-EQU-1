import unittest
from datetime import datetime,timedelta
from domain.model import *
from application.services import ServicioCitas
from infrastructure.memory import RepositorioCitasMemoria
T=datetime(2026,10,20,10)
class TestAplicacion(unittest.TestCase):
 def setUp(self):
    self.repo=RepositorioCitasMemoria();self.j=JornadaMedica('j','m','s',T,T+timedelta(hours=4),1)
    self.s=ServicioCitas(self.repo,[self.j],[])
 def nueva(self,id='1',paciente='p',inicio=T,medico='m',sucursal='s'):
    return Cita(id,paciente,medico,sucursal,inicio,inicio+timedelta(minutes=30))
 def test_reserva(self):self.assertEqual(self.s.reservar(self.nueva(),T).id,'1')
 def test_id_duplicado(self):
    self.s.reservar(self.nueva(),T)
    with self.assertRaises(ReglaNegocioError):self.s.reservar(self.nueva(),T)
 def test_paciente_duplicado_otra_sucursal(self):
    self.s.reservar(self.nueva(),T)
    with self.assertRaises(ReglaNegocioError):self.s.reservar(self.nueva('2','p',T,'otro','otra'),T)
 def test_medico_ocupado(self):
    self.s.reservar(self.nueva(),T)
    with self.assertRaises(ReglaNegocioError):self.s.reservar(self.nueva('2','otro'),T)
 def test_fuera_jornada(self):
    with self.assertRaises(ReglaNegocioError):self.s.reservar(self.nueva(inicio=T-timedelta(hours=1)),T)
 def test_retencion_ajena(self):
    self.s.retener('otro','m',T,T+timedelta(minutes=30),T)
    with self.assertRaises(ReglaNegocioError):self.s.reservar(self.nueva(),T)
 def test_retencion_propia(self):
    self.s.retener('p','m',T,T+timedelta(minutes=30),T);self.assertEqual(self.s.reservar(self.nueva(),T).id,'1')
 def test_retencion_vencida(self):
    self.s.retener('otro','m',T,T+timedelta(minutes=30),T-timedelta(minutes=3));self.s.reservar(self.nueva(),T)
 def test_cancelar(self):
    self.s.reservar(self.nueva(),T);self.s.cancelar('1','Paciente','recepcion',T);self.assertEqual(self.repo.obtener('1').estado,EstadoCita.CANCELADA)
 def test_llegada_y_atencion(self):
    self.s.reservar(self.nueva(),T);self.s.llegada('1',T);self.s.atender('1');self.assertEqual(self.repo.obtener('1').estado,EstadoCita.ATENDIDA)
 def test_ausencia(self):
    self.s.reservar(self.nueva(),T);self.s.ausencia('1',T+timedelta(minutes=20));self.assertEqual(self.repo.obtener('1').estado,EstadoCita.AUSENTE)
 def test_consulta(self):
    self.s.reservar(self.nueva(),T);self.assertEqual(len(self.s.consultar_paciente('p')),1)
 def test_cancelar_jornada(self):
    self.s.reservar(self.nueva(),T);self.s.cancelar_jornada(self.j,'empleado',T,True);self.assertEqual(self.repo.obtener('1').estado,EstadoCita.PENDIENTE_CONFIRMACION)
 def test_cita_inexistente(self):
    with self.assertRaises(ReglaNegocioError):self.s.cancelar('no','motivo','actor',T)
 def test_restriccion_remota(self):
    for i in range(3):
        c=self.nueva(str(i),inicio=T-timedelta(days=i+1));c.registrar_ausencia(c.inicio+timedelta(minutes=20));self.repo.guardar(c)
    with self.assertRaises(ReglaNegocioError):self.s.reservar(self.nueva('n',inicio=T+timedelta(hours=1)),T,'remoto')
 def test_anticipo_habilita(self):
    for i in range(3):
        c=self.nueva(str(i),inicio=T-timedelta(days=i+1));c.registrar_ausencia(c.inicio+timedelta(minutes=20));self.repo.guardar(c)
    self.s.reservar(self.nueva('n',inicio=T+timedelta(hours=1)),T,'remoto',True)
