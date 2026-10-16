import unittest
from datetime import datetime,timedelta
from domain.model import Cita
from infrastructure.serializacion import cita_resumen
class PruebasSerializacion(unittest.TestCase):
 def test_resumen(self):
  t=datetime(2026,10,20,9);c=Cita('c','p','m','s',t,t+timedelta(minutes=30))
  self.assertEqual(cita_resumen(c)['estado'],'reservada')
 def test_iso(self):
  t=datetime(2026,10,20,9);c=Cita('c','p','m','s',t,t+timedelta(minutes=30))
  self.assertIn('2026-10-20',cita_resumen(c)['inicio'])
