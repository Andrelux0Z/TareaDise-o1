from dataclasses import dataclass
import re

def validar_cedula(valor: str) -> bool:
    return bool(re.match(r'^\d-\d{4}-\d{4}$', valor))

@dataclass(frozen=True)
class Cedula:
    valor: str

@dataclass(frozen=True)
class Receta:
    cedula: Cedula

@dataclass(frozen=True)
class Despacho:
    folio: str
    cadena: str
    vence: str
