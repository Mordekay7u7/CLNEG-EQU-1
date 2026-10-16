import unittest
from datetime import datetime,timedelta
from domain.model import Retencion
from domain.retenciones import bloqueada,depurar
class PruebasRetenciones(unittest.TestCase):
 def setUp(self):
  self.t=datetime(2026,10,20,9)
  self.r=Retencion('p','m',self.t,self.t+timedelta(minutes=30),self.t)
 def test_bloqueo_otro_paciente(self): self.assertTrue(bloqueada([self.r],'m',self.t,self.t+timedelta(minutes=10),self.t,'otro'))
 def test_sin_bloqueo_propietario(self): self.assertFalse(bloqueada([self.r],'m',self.t,self.t+timedelta(minutes=10),self.t,'p'))
 def test_expira_tres_minutos(self): self.assertEqual(depurar([self.r],self.t+timedelta(minutes=3)),[])
