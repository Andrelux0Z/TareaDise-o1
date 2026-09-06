from typing import Protocol
import uuid

class Pasarela(Protocol):
    def enviar(self): ...

class Reloj(Protocol):
    def ahora(self): ...

class GeneradorFolio(Protocol):
    def siguiente(self): ...

class Bitacora(Protocol):
    def registrar(self): ...
