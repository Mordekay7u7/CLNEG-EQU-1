"""Caso de uso de cancelación."""
class CancelarCita:
    def __init__(self,servicio): self.servicio=servicio
    def ejecutar(self,id,motivo,actor,ahora): return self.servicio.cancelar(id,motivo,actor,ahora)
