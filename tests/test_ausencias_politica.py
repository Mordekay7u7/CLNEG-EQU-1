import unittest
from datetime import datetime,timedelta
from domain.model import Cita,EstadoCita
from domain.ausencias import contar,requiere_anticipo
class PruebasAusencias(unittest.TestCase):
 def setUp(self):
  self.t=datetime(2026,10,20,12)
  self.citas=[Cita(str(i),'p','m','s',self.t-timedelta(days=i),self.t-timedelta(days=i)+timedelta(minutes=30),EstadoCita.AUSENTE) for i in (1,2,3)]
 def test_cuenta_tres(self): self.assertEqual(contar(self.citas,'p',self.t),3)
 def test_restringe(self): self.assertTrue(requiere_anticipo(self.citas,'p',self.t))
 def test_otro_paciente(self): self.assertFalse(requiere_anticipo(self.citas,'otro',self.t))
