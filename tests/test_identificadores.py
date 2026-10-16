import unittest
from domain.identificadores import obligatorio
from domain.model import ReglaNegocioError
class PruebasIdentificadores(unittest.TestCase):
 def test_limpia_espacios(self): self.assertEqual(obligatorio('  P01  ','Paciente'),'P01')
 def test_vacio(self):
  with self.assertRaises(ReglaNegocioError): obligatorio('  ','Paciente')
 def test_tipo_incorrecto(self):
  with self.assertRaises(ReglaNegocioError): obligatorio(None,'Paciente')
