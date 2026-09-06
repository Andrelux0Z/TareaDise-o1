from datetime import timedelta
from clinicasegura.dominio.modelos import Receta, Despacho
from clinicasegura.dominio.errores import CadenaNoSoportada, FarmaciaNoDisponible

class EmisionDeRecetas:
    def __init__(self, pasarelas, reloj, folios, bitacora):
        self.pasarelas = pasarelas
        self.reloj = reloj
        self.folios = folios
        self.bitacora = bitacora

    def emitir(self, receta: Receta, cadena: str) -> Despacho:
        pasarela = self.pasarelas.get(cadena)
        if not pasarela:
            raise CadenaNoSoportada()
        folio = self.folios.siguiente()
        vence = self.reloj.ahora() + timedelta(days=receta.dias)
        try:
            despacho = pasarela.enviar(receta, folio, vence)
        except Exception as e:
            self.bitacora.registrar(f'fallo_{cadena}', folio)
            raise FarmaciaNoDisponible(f'Fallo en {cadena}') from e
        self.bitacora.registrar('emitida', folio)
        return despacho
