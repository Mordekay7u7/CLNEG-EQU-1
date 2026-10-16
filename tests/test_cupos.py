import unittest
from datetime import datetime,timedelta
from domain.model import Cita,JornadaMedica
from domain.cupos import ocupacion,lugares_disponibles
class PruebasCupos(unittest.TestCase):
 def setUp(self):
  self.t=datetime(2026,10,20,9)
  self.j=JornadaMedica('j','m','s',self.t,self.t+timedelta(hours=4),2)
  self.c=Cita('c','p','m','s',self.t,self.t+timedelta(minutes=30))
 def test_sin_ocupacion(self): self.assertEqual(ocupacion(self.j,[]),0)
 def test_una_ocupada(self): self.assertEqual(ocupacion(self.j,[self.c]),1)
 def test_una_disponible(self): self.assertEqual(lugares_disponibles(self.j,[self.c]),1)
