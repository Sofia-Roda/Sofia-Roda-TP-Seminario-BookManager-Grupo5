import os
from typing import Dict, Optional

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


# Ruta absoluta a la carpeta de los CSV, para que funcione sin importar
# desde qué directorio se ejecute el programa.
RUTA_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "migrations",
    "csv",
)


def ruta_csv(nombre_archivo: str) -> str:
    """Devuelve la ruta completa de un archivo de la carpeta de CSV."""
    return os.path.join(RUTA_CSV, nombre_archivo)


def crear_repositorios(persistir: bool = False) -> Dict[str, object]:
    """Crea los repositorios necesarios para la aplicación.

    Si persistir es True, cada repositorio lee su archivo CSV al crearse
    y guarda en él cada cambio. Si es False, los repositorios arrancan
    vacíos y solo trabajan en memoria.

    Se crean en orden de dependencia: los libros necesitan géneros y
    editoriales ya cargados, los precios necesitan libros y monedas, etc.
    """
    def ruta(nombre_archivo: str) -> Optional[str]:
        return ruta_csv(nombre_archivo) if persistir else None

    generos = RepositorioGenero(ruta("generos.csv"))
    editoriales = RepositorioEditorial(ruta("editoriales.csv"))
    monedas = RepositorioMoneda(ruta("monedas.csv"))
    tipos_cotizacion = RepositorioTipoCotizacion(ruta("tipos_cotizacion.csv"))
    libros = RepositorioLibro(generos, editoriales, ruta("libros.csv"))

    return {
        "generos": generos,
        "editoriales": editoriales,
        "monedas": monedas,
        "tipos_cotizacion": tipos_cotizacion,
        "libros": libros,
        "precios": RepositorioPrecio(libros, monedas, ruta("precios.csv")),
        "stock": RepositorioStock(libros, ruta("stock.csv")),
        "cotizaciones": RepositorioCotizacionDolar(
            tipos_cotizacion, ruta("cotizaciones_dolar.csv")
        ),
    }


def cargar_datos_iniciales() -> Dict[str, object]:
    """Crea los repositorios cargando los datos guardados en los CSV."""
    return crear_repositorios(persistir=True)
