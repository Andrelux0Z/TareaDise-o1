from decimal import Decimal

def calcular_recargo(dias_restantes: int, tarifa_diaria: Decimal, recargo_por_riesgo: bool) -> Decimal:
    if recargo_por_riesgo:
        return Decimal(dias_restantes) * tarifa_diaria * Decimal(2)
    return Decimal(dias_restantes) * tarifa_diaria
