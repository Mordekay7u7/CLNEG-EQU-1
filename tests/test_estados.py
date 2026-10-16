import unittest
from domain.estados import ACTIVAS,TERMINALES
from domain.model import EstadoCita
class PruebasEstados(unittest.TestCase):
 def test_reservada_activa(self): self.assertIn(EstadoCita.RESERVADA,ACTIVAS)
 def test_pendiente_activa(self): self.assertIn(EstadoCita.PENDIENTE_CONFIRMACION,ACTIVAS)
 def test_cancelada_terminal(self): self.assertIn(EstadoCita.CANCELADA,TERMINALES)
 def test_ausente_terminal(self): self.assertIn(EstadoCita.AUSENTE,TERMINALES)
