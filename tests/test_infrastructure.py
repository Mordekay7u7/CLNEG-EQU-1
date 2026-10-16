import unittest
from datetime import datetime,timedelta
from domain.model import Cita,EstadoCita
from infrastructure.memory import RepositorioCitasMemoria,UnidadTrabajoMemoria
class TestInfraestructura(unittest.TestCase):
 def setUp(self):
    self.repo=RepositorioCitasMemoria();t=datetime(2026,10,20,10);self.c=Cita('1','p','m','s',t,t+timedelta(minutes=30))
 def test_guardar_y_obtener(self):
    self.repo.guardar(self.c);self.assertEqual(self.repo.obtener('1').paciente_id,'p')
 def test_copia_aislada(self):
    self.repo.guardar(self.c);c=self.repo.obtener('1');c.estado=EstadoCita.CANCELADA;self.assertEqual(self.repo.obtener('1').estado,EstadoCita.RESERVADA)
 def test_rollback_sin_confirmar(self):
    with UnidadTrabajoMemoria(self.repo):self.repo.guardar(self.c)
    self.assertIsNone(self.repo.obtener('1'))
 def test_commit(self):
    with UnidadTrabajoMemoria(self.repo) as u:self.repo.guardar(self.c);u.confirmar()
    self.assertIsNotNone(self.repo.obtener('1'))
 def test_rollback_excepcion(self):
    with self.assertRaises(RuntimeError):
        with UnidadTrabajoMemoria(self.repo):self.repo.guardar(self.c);raise RuntimeError('error')
    self.assertIsNone(self.repo.obtener('1'))
