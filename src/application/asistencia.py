"""Casos de uso de llegada y atención."""
class RegistrarAsistencia:
    def __init__(self,servicio): self.servicio=servicio
    def llegada(self,id,ahora,autorizada=False): return self.servicio.llegada(id,ahora,autorizada)
    def atender(self,id): return self.servicio.atender(id)
    def ausencia(self,id,ahora): return self.servicio.ausencia(id,ahora)
