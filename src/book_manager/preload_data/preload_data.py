import os
from typing import Dict

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from book_manager.database.connection import ConexionDB
from book_manager.models.models import Base, GeneroModel
from book_manager.repositories.repositories import (
    RepositorioCotizacionDolar,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)


RUTA_SQL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "migrations",
    "sql",
)

ORDEN_TABLAS = [
    "generos",
    "editoriales",
    "monedas",
    "tipos_cotizacion",
    "libros",
    "precios",
    "stock",
    "cotizaciones_dolar",
]


def crear_repositorios(conexion: ConexionDB) -> Dict[str, object]:
    """Crea los repositorios necesarios para la aplicación."""
    Base.metadata.create_all(conexion.engine)

    generos = RepositorioGenero(conexion)
    editoriales = RepositorioEditorial(conexion)
    monedas = RepositorioMoneda(conexion)
    tipos_cotizacion = RepositorioTipoCotizacion(conexion)
    libros = RepositorioLibro(conexion, generos, editoriales)

    return {
        "generos": generos,
        "editoriales": editoriales,
        "monedas": monedas,
        "tipos_cotizacion": tipos_cotizacion,
        "libros": libros,
        "precios": RepositorioPrecio(conexion, libros, monedas),
        "stock": RepositorioStock(conexion, libros),
        "cotizaciones": RepositorioCotizacionDolar(conexion, tipos_cotizacion),
    }


def cargar_datos_desde_sql(sesion: Session, ruta_archivo: str) -> int:
    """Ejecuta las sentencias de un archivo .sql dentro de una sesión.

    Se ignoran las líneas vacías y los comentarios (líneas que comienzan
    con "--"). Cada sentencia termina con ";" y puede ocupar una o más
    líneas. La confirmación de los cambios queda a cargo de quien maneja
    la sesión, para poder cargar varios archivos en una misma transacción.

    Args:
        sesion (Session): Sesión de SQLAlchemy donde se ejecutan las
            sentencias.
        ruta_archivo (str): Ruta del archivo .sql a cargar.

    Returns:
        int: Cantidad de sentencias ejecutadas.

    Raises:
        FileNotFoundError: Si no existe el archivo indicado.
    """
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo SQL: {ruta_archivo}"
        )

    cantidad = 0
    sentencia = ""
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith("--"):
                continue
            sentencia = f"{sentencia} {linea}".strip()
            if sentencia.endswith(";"):
                sesion.execute(text(sentencia))
                cantidad += 1
                sentencia = ""

    if sentencia:
        sesion.execute(text(sentencia))
        cantidad += 1

    return cantidad


def cargar_datos_iniciales(conexion: ConexionDB) -> Dict[str, object]:
    """Crea los repositorios y carga los datos de la migración."""
    repositorios = crear_repositorios(conexion)

    with conexion.transaccion() as sesion:
        cantidad = sesion.execute(
            select(func.count()).select_from(GeneroModel)
        ).scalar()
        if cantidad == 0:
            for tabla in ORDEN_TABLAS:
                ruta = os.path.join(RUTA_SQL, f"{tabla}.sql")
                cargar_datos_desde_sql(sesion, ruta)

    return repositorios
