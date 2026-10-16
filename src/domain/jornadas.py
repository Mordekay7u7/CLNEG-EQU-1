"""Consultas sobre jornadas disponibles."""
def jornada_de(cita,jornadas): return next((j for j in jornadas if j.contiene(cita)),None)
def jornadas_activas(jornadas): return [j for j in jornadas if not j.cancelada]
