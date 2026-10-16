"""Resumen de citas de la clínica."""
from collections import Counter
def resumen_estados(citas): return dict(Counter(c.estado.value for c in citas))
def total_citas(citas): return len(citas)
