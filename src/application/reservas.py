"""Caso de uso de reserva."""
class ReservarCita:
    def __init__(self,servicio): self.servicio=servicio
    def ejecutar(self,cita,ahora,**opciones): return self.servicio.reservar(cita,ahora,**opciones)
