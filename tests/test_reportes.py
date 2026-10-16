import unittest
from datetime import datetime,timedelta
from domain.model import Cita
from application.reportes import resumen_estados,total_citas
class PruebasReportes(unittest.TestCase):
 def test_vacio(self): self.assertEqual(resumen_estados([]),{})
 def test_total(self):
  t=datetime(2026,10,20,9);c=Cita('c','p','m','s',t,t+timedelta(minutes=30))
  self.assertEqual(total_citas([c]),1)
  self.assertEqual(resumen_estados([c])['reservada'],1)
