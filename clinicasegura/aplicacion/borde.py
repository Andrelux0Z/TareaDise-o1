from pydantic import BaseModel, ConfigDict, Field, field_validator
from clinicasegura.dominio.modelos import Receta, Cedula
from decimal import Decimal
import re

class SolicitudReceta(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    cedula: str
    medicamento: str
    dias: int = Field(gt=0, le=90)
    dosis_mg: str

    @field_validator('cedula')
    @classmethod
    def validar_cedula_formato(cls, v: str) -> str:
        if not re.match(r'^\d-\d{4}-\d{4}$', v):
            raise ValueError('la cédula tiene formato 0-0000-0000')
        return v

    @field_validator('dosis_mg')
    @classmethod
    def validar_dosis(cls, v: str) -> str:
        if Decimal(v) <= 0:
            raise ValueError('la dosis debe ser positiva')
        return v

def a_receta(solicitud: SolicitudReceta) -> Receta:
    return Receta(
        cedula=Cedula(solicitud.cedula),
        medicamento=solicitud.medicamento,
        dias=solicitud.dias,
        dosis_mg=Decimal(solicitud.dosis_mg)
    )