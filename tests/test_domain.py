import unittest
from datetime import datetime,timedelta
from domain.model import *
T=datetime(2026,10,20,10)
def cita(id='1'):return Cita(id,'p','m','s',T,T+timedelta(minutes=30))
class TestDominio(unittest.TestCase):
    def test_cita_valida(self):self.assertEqual(cita().estado,EstadoCita.RESERVADA)
    def test_horario_invalido(self):
        with self.assertRaises(ReglaNegocioError):Cita('1','p','m','s',T,T)
    def test_identificador_vacio(self):
        with self.assertRaises(ReglaNegocioError):Cita('','p','m','s',T,T+timedelta(minutes=30))
    def test_cancelacion_auditada(self):
        c=cita();c.cancelar('Solicitud','recepcion',T);self.assertEqual((c.estado,c.cancelada_por),(EstadoCita.CANCELADA,'recepcion'))
    def test_cancelacion_sin_motivo(self):
        with self.assertRaises(ReglaNegocioError):cita().cancelar('','recepcion',T)
    def test_doble_cancelacion(self):
        c=cita();c.cancelar('Solicitud','recepcion',T)
        with self.assertRaises(ReglaNegocioError):c.cancelar('otra','recepcion',T)
    def test_llegada_en_limite(self):
        c=cita();c.registrar_llegada(T+timedelta(minutes=15));self.assertIsNotNone(c.llegada)
    def test_llegada_tarde_sin_permiso(self):
        with self.assertRaises(ReglaNegocioError):cita().registrar_llegada(T+timedelta(minutes=16))
    def test_llegada_tarde_autorizada(self):
        c=cita();c.registrar_llegada(T+timedelta(minutes=16),True);self.assertTrue(c.validacion_medico)
    def test_ausencia_antes_de_20(self):
        with self.assertRaises(ReglaNegocioError):cita().registrar_ausencia(T+timedelta(minutes=19))
    def test_ausencia_a_los_20(self):
        c=cita();c.registrar_ausencia(T+timedelta(minutes=20));self.assertEqual(c.estado,EstadoCita.AUSENTE)
    def test_atender_sin_llegada(self):
        with self.assertRaises(ReglaNegocioError):cita().atender()
    def test_atender_con_llegada(self):
        c=cita();c.registrar_llegada(T);c.atender();self.assertEqual(c.estado,EstadoCita.ATENDIDA)
    def test_retencion_tres_minutos(self):
        r=Retencion('p','m',T,T+timedelta(minutes=30),T);self.assertTrue(r.vigente(T+timedelta(minutes=2,seconds=59)));self.assertFalse(r.vigente(T+timedelta(minutes=3)))
    def test_solapamiento_limite(self):self.assertFalse(solapan(T,T+timedelta(minutes=30),T+timedelta(minutes=30),T+timedelta(minutes=60)))
    def test_jornada_invalida(self):
        with self.assertRaises(ReglaNegocioError):JornadaMedica('j','m','s',T,T,1)
    def test_sobrecupo_maximo(self):
        j=JornadaMedica('j','m','s',T,T+timedelta(hours=4),1);j.permitir_sobrecupo(True);j.permitir_sobrecupo(True)
        with self.assertRaises(ReglaNegocioError):j.permitir_sobrecupo(True)
    def test_sobrecupo_sin_autorizacion(self):
        with self.assertRaises(ReglaNegocioError):JornadaMedica('j','m','s',T,T+timedelta(hours=4),1).permitir_sobrecupo(False)
    def test_empleado_requiere_justificante(self):
        with self.assertRaises(ReglaNegocioError):JornadaMedica('j','m','s',T,T+timedelta(hours=4),1).cancelar('empleado',T)
    def test_honorarios_24_horas(self):
        with self.assertRaises(ReglaNegocioError):JornadaMedica('j','m','s',T,T+timedelta(hours=4),1).cancelar('honorarios',T-timedelta(hours=23))
    def test_honorarios_24_horas_exacto(self):
        j=JornadaMedica('j','m','s',T,T+timedelta(hours=4),1);j.cancelar('honorarios',T-timedelta(hours=24));self.assertTrue(j.cancelada)
    def test_restriccion_tres_ausencias(self):
        citas=[cita(str(i)) for i in range(3)]
        for c in citas:c.registrar_ausencia(T+timedelta(minutes=20))
        self.assertTrue(restringido_por_ausencias(citas,'p',T+timedelta(days=1)))
