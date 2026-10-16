"""Transacción local simulada para pruebas de commit y rollback."""
from copy import deepcopy
class UnidadTrabajoMemoria:
    def __init__(self,repositorio):
        self.repositorio=repositorio;self._instantanea=None;self.confirmada=False
    def __enter__(self):
        self._instantanea=deepcopy(self.repositorio.__dict__);self.confirmada=False;return self
    def confirmar(self):self.confirmada=True
    def revertir(self):
        if self._instantanea is not None:self.repositorio.__dict__.clear();self.repositorio.__dict__.update(deepcopy(self._instantanea))
        self.confirmada=False
    def __exit__(self,tipo,error,traza):
        if tipo is not None or not self.confirmada:self.revertir()
        return False
