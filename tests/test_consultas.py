import unittest
from datetime import datetime,timedelta
from infrastructure.memory import RepositorioCitasMemoria
from domain.model import Cita,EstadoCita
from application.consultas import por_estado,por_medico,por_sucursal
class PruebasConsultas(unittest.TestCase):
 def setUp(self):
  self.r=RepositorioCitasMemoria();t=datetime(2026,10,20,9)
  self.r.guardar(Cita('c','p','m','s',t,t+timedelta(minutes=30)))
 def test_por_estado(self): self.assertEqual(len(por_estado(self.r,EstadoCita.RESERVADA)),1)
 def test_por_medico(self): self.assertEqual(len(por_medico(self.r,'m')),1)
 def test_por_sucursal(self): self.assertEqual(len(por_sucursal(self.r,'otra')),0)
