"""Generar el reporte en Excel con la comparación de precios."""
import datetime
from pathlib import Path
from typing import List

import pandas as pd

from book_manager.scraper.comparador import RUTA_REPORTES

COLUMNAS = {
    "titulo": "Libro",
    "precio_interno": "Precio interno",
    "precio_web": "Precio web",
    "diferencia": "Diferencia",
    "fecha_extraccion": "Fecha de extracción",
}


def generar_reporte_excel(comparaciones: List[dict]) -> Path:
    """Genera un archivo Excel con la comparación de precios.

    Args:
        comparaciones (List[dict]): Comparaciones devueltas por
            `comparar_precios_y_generar_alertas`, cada una con titulo,
            precio_interno, precio_web, diferencia y fecha_extraccion.

    Returns:
        Path: Ruta del archivo Excel generado.

    Raises:
        ValueError: Si no hay comparaciones para incluir en el reporte.
    """
    if not comparaciones:
        raise ValueError("No hay comparaciones para generar el reporte.")

    tabla = pd.DataFrame(comparaciones)
    tabla = tabla[list(COLUMNAS)].rename(columns=COLUMNAS)

    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    ruta_excel = (
        RUTA_REPORTES / f"reporte_precios_{datetime.date.today().isoformat()}.xlsx"
    )
    tabla.to_excel(ruta_excel, index=False)

    print(f"Se generó el reporte en {ruta_excel}")
    return ruta_excel
