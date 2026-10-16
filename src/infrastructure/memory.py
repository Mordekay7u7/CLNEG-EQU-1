"""Adaptador local de referencia; no representa una BD clínica."""
from copy import deepcopy
class RepositorioCitasMemoria:
    def __init__(self): self._datos={}
    def obtener(self,id): return deepcopy(self._datos.get(id))
    def listar(self): return deepcopy(list(self._datos.values()))
    def guardar(self,cita): self._datos[cita.id]=deepcopy(cita)
    def snapshot(self): return deepcopy(self._datos)
    def restaurar(self,snapshot): self._datos=deepcopy(snapshot)
class UnidadTrabajoMemoria:
    def __init__(self,repo): self.repo=repo;self._copia=None
    def __enter__(self): self._copia=self.repo.snapshot();return self
    def confirmar(self): self._copia=None
    def __exit__(self,tipo,valor,trace):
        if self._copia is not None:self.repo.restaurar(self._copia)
        return False
