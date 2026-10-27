"""Comparar los precios internos con los precios de Cúspide."""
import csv
import datetime
import json
import subprocess
from pathlib import Path
from typing import Dict, List

from book_manager.services.services import LibroService, PrecioService

RUTA_SCRAPER = Path(__file__).resolve().parent
RUTA_REPORTES = Path(__file__).resolve().parents[1] / "reportes"


def obtener_precios_web(titulos: List[str]) -> List[dict]:
    """Ejecuta el spider de Cúspide y devuelve los resultados obtenidos.

    Args:
        titulos (List[str]): Títulos de libros a buscar en Cúspide.

    Returns:
        List[dict]: Todos los resultados encontrados (puede haber más de
            uno por título, si Cúspide tiene varias ediciones).

    Raises:
        RuntimeError: Si la ejecución del scraper falla.
    """
    if not titulos:
        return []

    ruta_salida = RUTA_SCRAPER / "resultado_comparacion.json"
    ruta_salida.unlink(missing_ok=True)

    comando = [
        "scrapy",
        "crawl",
        "cuspide",
        "-a",
        f"titulos={';'.join(titulos)}",
        "-o",
        str(ruta_salida),
    ]

    resultado = subprocess.run(
        comando,
        cwd=RUTA_SCRAPER,
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:
        raise RuntimeError(f"Error al ejecutar el scraper: {resultado.stderr}")

    if not ruta_salida.exists():
        return []

    with open(ruta_salida, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def comparar_precios_y_generar_alertas(
    libro_service: LibroService,
    precio_service: PrecioService,
    diferencia_minima: float,
) -> tuple[Path, List[dict]]:
    """Compara el precio interno de cada libro con el precio web y genera alertas.

    Para cada libro del catálogo con precio en pesos argentinos, busca su
    precio en Cúspide. Si Cúspide tiene más de un resultado para el mismo
    título (por ejemplo, ediciones de autores distintos), se tratan por
    separado: se genera una alerta por cada coincidencia cuya diferencia
    de precio sea mayor o igual a `diferencia_minima`.

    Args:
        libro_service (LibroService): Servicio para listar los libros.
        precio_service (PrecioService): Servicio para listar los precios.
        diferencia_minima (float): Diferencia mínima para generar una alerta.

    Returns:
        tuple[Path, List[dict]]: La ruta del CSV generado y la lista de
            alertas (cada una con libro_id, titulo, precio_interno,
            precio_web, diferencia y url), para que otras partes del
            sistema (por ejemplo, el reporte en Excel) puedan reusarlas
            sin tener que volver a leer el archivo.

    Raises:
        ValueError: Si `diferencia_minima` es negativa.
    """
    if diferencia_minima < 0:
        raise ValueError("La diferencia mínima no puede ser negativa.")

    libros = libro_service.listar()

    precios_internos: Dict[int, float] = {
        precio.libro.id: precio.valor
        for precio in precio_service.listar()
        if precio.moneda.codigo == "ARS"
    }

    libros_con_precio = [libro for libro in libros if libro.id in precios_internos]
    titulos = [libro.titulo for libro in libros_con_precio]

    resultados_web = obtener_precios_web(titulos)

    resultados_por_titulo: Dict[str, List[dict]] = {}
    for resultado in resultados_web:
        resultados_por_titulo.setdefault(resultado["titulo_buscado"], []).append(
            resultado
        )

    alertas: List[dict] = []

    for libro in libros_con_precio:
        coincidencias = resultados_por_titulo.get(libro.titulo, [])

        if len(coincidencias) > 1:
            print(
                f"'{libro.titulo}' tiene {len(coincidencias)} coincidencias "
                "en Cúspide, se muestran todas por separado."
            )

        precio_interno = precios_internos[libro.id]

        for resultado in coincidencias:
            precio_web = resultado["precio"]
            diferencia = abs(precio_interno - precio_web)

            if diferencia >= diferencia_minima:
                alertas.append(
                    {
                        "libro_id": libro.id,
                        "titulo": libro.titulo,
                        "precio_interno": precio_interno,
                        "precio_web": precio_web,
                        "diferencia": diferencia,
                        "url": resultado["url"],
                    }
                )

    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    ruta_csv = RUTA_REPORTES / f"alertas_{datetime.date.today().isoformat()}.csv"

    with open(ruta_csv, "w", encoding="utf-8", newline="") as archivo_csv:
        columnas = ["libro_id", "titulo", "precio_interno", "precio_web", "diferencia", "url"]
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(alertas)

    print(f"Se generaron {len(alertas)} alerta(s) en {ruta_csv}")

    return ruta_csv, alertas