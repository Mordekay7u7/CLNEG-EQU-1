"""Clasificación de llegadas a consulta."""
from datetime import timedelta
def tardia(inicio,llegada): return llegada>inicio+timedelta(minutes=15)
def corresponde_ausencia(inicio,ahora): return ahora>=inicio+timedelta(minutes=20)
