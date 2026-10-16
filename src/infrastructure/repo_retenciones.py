"""Repositorio de retenciones con expiración."""
from copy import deepcopy
class RepositorioRetenciones:
    def __init__(self): self._datos=[]
    def guardar(self,retencion): self._datos.append(deepcopy(retencion))
    def vigentes(self,ahora): return deepcopy([r for r in self._datos if r.vigente(ahora)])
