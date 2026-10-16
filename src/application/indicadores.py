"""Indicadores derivados de datos sintéticos, no indicadores clínicos reales."""
from domain.model import EstadoCita
def indicadores_citas(citas):
    datos=list(citas); n=len(datos)
    def cuenta(estado):return sum(c.estado==estado for c in datos)
    return {'total':n,'atendidas':cuenta(EstadoCita.ATENDIDA),'ausentes':cuenta(EstadoCita.AUSENTE),
            'canceladas':cuenta(EstadoCita.CANCELADA),'reservadas':cuenta(EstadoCita.RESERVADA),
            'porcentaje_ausencias':round(100*cuenta(EstadoCita.AUSENTE)/n,2) if n else 0.0}
