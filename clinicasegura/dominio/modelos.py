from dataclasses import dataclass
import re
from decimal import Decimal

def validar_cedula(valor: str) -> bool:
    return bool(re.match(r'^\d-\d{4}-\d{4}$', valor))

@dataclass(frozen=True)
class Cedula:
    valor: str

@dataclass(frozen=True)
class Receta:
    cedula: Cedula
    medicamento: str
    dias: int
    dosis_mg: Decimal

@dataclass(frozen=True)
class Despacho:
    folio: str
    cadena: str
    vence: str
