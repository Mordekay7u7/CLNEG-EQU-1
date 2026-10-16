import unittest
from infrastructure.fabrica import crear_servicio
class PruebasFabrica(unittest.TestCase):
 def test_servicio_creado(self): self.assertEqual(crear_servicio().repo.listar(),[])
 def test_jornadas_iniciales(self): self.assertEqual(crear_servicio([]).jornadas,[])
