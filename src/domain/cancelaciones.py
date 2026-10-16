"""Validación de motivos y responsables."""
from .identificadores import obligatorio
def validar_auditoria(motivo,actor): return obligatorio(motivo,'Motivo'),obligatorio(actor,'Responsable')
