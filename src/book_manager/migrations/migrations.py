import csv
import os
from typing import Dict, List, Set


# Orden de migración: las tablas "padre" (sin dependencias) primero,
# cuando se inserten las tablas que tienen claves foráneas (libros,
# precios, stock, cotizaciones_dolar) ya existen las filas a las que
# apuntan.
ORDEN_TABLAS: List[str] = [
    "generos",
    "editoriales",
    "monedas",
    "tipos_cotizacion",
    "libros",
    "precios",
    "stock",
    "cotizaciones_dolar",
]


COLUMNAS_NUMERICAS: Dict[str, Set[str]] = {
    "generos": {"id"},
    "editoriales": {"id"},
    "monedas": {"id"},
    "tipos_cotizacion": {"id"},
    "libros": {"id", "genero_id", "editorial_id", "num_paginas", "peso", "ranking"},
    "precios": {"id", "libro_id", "moneda_id", "valor"},
    "stock": {"id", "libro_id", "cantidad"},
    "cotizaciones_dolar": {"id", "tipo_cotizacion_id", "valor"},
}


def _formatear_valor(nombre_tabla: str, nombre_columna: str, valor: str) -> str:
    """Da formato SQL a un valor leído del CSV (siempre llega como texto)."""
    if valor == "":
        return "NULL"
    if nombre_columna in COLUMNAS_NUMERICAS.get(nombre_tabla, set()):
        return valor
    texto_escapado = valor.replace("'", "''")
    return f"'{texto_escapado}'"


def _generar_inserts(nombre_tabla: str, ruta_csv: str) -> List[str]:
    """Genera las sentencias INSERT INTO para una tabla a partir de su CSV."""
    sentencias: List[str] = []

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        columnas = lector.fieldnames

        for fila in lector:
            valores = ", ".join(
                _formatear_valor(nombre_tabla, columna, fila[columna])
                for columna in columnas
            )
            columnas_sql = ", ".join(columnas)
            sentencias.append(
                f"INSERT INTO {nombre_tabla} ({columnas_sql}) VALUES ({valores});"
            )

    return sentencias


def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> None:
    """Función encargada de la migración de datos de csv a sql.

    Se encarga de leer los archivos csv y crear los archivos sql
    para la inserción en la base de datos.

    Args:
        carpeta_csvs (str): Carpeta donde se encuentran los archivos csv de origen.
        carpeta_sqls (str): Carpeta donde se deben guardar los archivos sql generados.
    """
    os.makedirs(carpeta_sqls, exist_ok=True)

    for nombre_tabla in ORDEN_TABLAS:
        ruta_csv = os.path.join(carpeta_csvs, f"{nombre_tabla}.csv")

        if not os.path.exists(ruta_csv):
            raise FileNotFoundError(f"No se encontró el archivo CSV: {ruta_csv}")

        sentencias = _generar_inserts(nombre_tabla, ruta_csv)

        ruta_sql = os.path.join(carpeta_sqls, f"{nombre_tabla}.sql")
        with open(ruta_sql, "w", encoding="utf-8", newline="") as archivo_sql:
            archivo_sql.write(f"-- Inserts generados a partir de {nombre_tabla}.csv\n")
            archivo_sql.write("\n".join(sentencias))
            archivo_sql.write("\n")

        print(f"{nombre_tabla}.sql generado ({len(sentencias)} filas).")