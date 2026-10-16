"""Adaptadores simulados: no envían mensajes ni manejan información real."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Notificacion:
    destinatario:str; asunto:str; mensaje:str
class NotificadorMemoria:
    def __init__(self):self.enviadas=[]
    def enviar(self,destinatario,asunto,mensaje):
        if not destinatario or not asunto:raise ValueError('Destinatario y asunto obligatorios')
        aviso=Notificacion(destinatario,asunto,mensaje);self.enviadas.append(aviso);return aviso
class RelojFijo:
    def __init__(self,ahora):self._ahora=ahora
    def ahora(self):return self._ahora
    def avanzar(self,delta):self._ahora+=delta
