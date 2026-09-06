import os
from clinicasegura.dominio.servicio import EmisionDeRecetas

def construir_servicio():
    timeout = int(os.environ.get('FARMACIA_TIMEOUT_MS', '1500'))
    return EmisionDeRecetas(pasarelas={}, reloj=None, folios=None, bitacora=None)
