import unittest
from application.validacion import canal_valido
from domain.model import ReglaNegocioError
class PruebasValidacion(unittest.TestCase):
 def test_recepcion(self): self.assertEqual(canal_valido('recepcion'),'recepcion')
 def test_whatsapp(self): self.assertEqual(canal_valido('whatsapp'),'whatsapp')
 def test_desconocido(self):
  with self.assertRaises(ReglaNegocioError): canal_valido('desconocido')
