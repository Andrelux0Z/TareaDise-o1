from clinicasegura.dominio.modelos import Receta, Despacho
from clinicasegura.dominio.errores import CadenaNoSoportada

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
        vence = self.reloj.ahora()
        return pasarela.enviar(receta, folio, vence)
