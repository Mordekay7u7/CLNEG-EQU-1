from datetime import datetime,timedelta
from domain.intervalos import Intervalo
from domain.model import ReglaNegocioError
import unittest
class PruebasIntervalos(unittest.TestCase):
 def setUp(self): self.t=datetime(2026,10,20,9)
 def test_duracion(self): self.assertEqual(Intervalo(self.t,self.t+timedelta(minutes=30)).minutos,30)
 def test_invalido(self):
  with self.assertRaises(ReglaNegocioError): Intervalo(self.t,self.t)
 def test_solapamiento(self):
  a=Intervalo(self.t,self.t+timedelta(minutes=30))
  self.assertTrue(a.coincide(Intervalo(self.t+timedelta(minutes=10),self.t+timedelta(minutes=40))))
 def test_contiguos(self):
  a=Intervalo(self.t,self.t+timedelta(minutes=30))
  self.assertFalse(a.coincide(Intervalo(self.t+timedelta(minutes=30),self.t+timedelta(minutes=60))))
 def test_contiene(self):
  a=Intervalo(self.t,self.t+timedelta(hours=2))
  self.assertTrue(a.contiene(Intervalo(self.t+timedelta(minutes=10),self.t+timedelta(minutes=40))))
