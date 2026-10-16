import unittest
from datetime import datetime,timedelta
from domain.model import JornadaMedica,Retencion
from infrastructure.repo_jornadas import RepositorioJornadas
from infrastructure.repo_retenciones import RepositorioRetenciones
class PruebasRepositorios(unittest.TestCase):
 def setUp(self): self.t=datetime(2026,10,20,9)
 def test_jornada_guardar(self):
  r=RepositorioJornadas();r.guardar(JornadaMedica('j','m','s',self.t,self.t+timedelta(hours=2),2))
  self.assertEqual(len(r.listar()),1)
 def test_jornada_aislada(self):
  r=RepositorioJornadas();r.guardar(JornadaMedica('j','m','s',self.t,self.t+timedelta(hours=2),2))
  j=r.obtener('j');j.capacidad=99
  self.assertEqual(r.obtener('j').capacidad,2)
 def test_retencion_vigente(self):
  r=RepositorioRetenciones();r.guardar(Retencion('p','m',self.t,self.t+timedelta(minutes=30),self.t))
  self.assertEqual(len(r.vigentes(self.t+timedelta(minutes=2))),1)
 def test_retencion_expirada(self):
  r=RepositorioRetenciones();r.guardar(Retencion('p','m',self.t,self.t+timedelta(minutes=30),self.t))
  self.assertEqual(len(r.vigentes(self.t+timedelta(minutes=3))),0)
