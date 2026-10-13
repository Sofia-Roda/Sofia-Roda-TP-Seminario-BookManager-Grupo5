import os
from typing import Dict

from sqlalchemy import func, select, text

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
                with open(ruta, "r", encoding="utf-8") as archivo:
                    for sentencia in archivo:
                        sentencia = sentencia.strip()
                        if sentencia and not sentencia.startswith("--"):
                            sesion.execute(text(sentencia))

    return repositorios
