"""Repositorio simulado de jornadas."""
from copy import deepcopy
class RepositorioJornadas:
    def __init__(self): self._datos={}
    def guardar(self,jornada): self._datos[jornada.id]=deepcopy(jornada)
    def obtener(self,id): return deepcopy(self._datos.get(id))
    def listar(self): return deepcopy(list(self._datos.values()))
