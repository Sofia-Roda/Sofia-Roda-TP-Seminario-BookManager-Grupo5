from typing import Dict

from book_manager.database.connection import ConexionDB
from book_manager.preload_data.preload_data import (
    cargar_datos_iniciales,
    crear_repositorios,
)
from book_manager.services.services import (
    CotizacionDolarService,
    EditorialService,
    GeneroService,
    LibroService,
    MonedaService,
    PrecioService,
    StockService,
    TipoCotizacionService,
)
from book_manager.ui.console import iniciar_menu
from book_manager.auditoria import AuditoriaService

def crear_servicios(repositorios: Dict[str, object]) -> Dict[str, object]:
    """Instancia los servicios de negocio a partir de los repositorios."""
    auditorias = AuditoriaService(repositorios["auditorias"])

    generos = GeneroService(
        repositorios["generos"],
        repositorios["libros"],
        auditorias,
    )

    editoriales = EditorialService(
        repositorios["editoriales"],
        repositorios["libros"],
        auditorias,
    )

    monedas = MonedaService(
        repositorios["monedas"],
        repositorios["precios"],
        auditorias,
    )

    tipos_cotizacion = TipoCotizacionService(
        repositorios["tipos_cotizacion"],
        repositorios["cotizaciones"],
        auditorias,
    )

    libros = LibroService(
        repositorios["libros"],
        generos,
        editoriales,
        repositorios["precios"],
        repositorios["stock"],
        auditorias,
    )

    precios = PrecioService(
        repositorios["precios"],
        libros,
        monedas,
        auditorias,
    )

    stock = StockService(
        repositorios["stock"],
        libros,
        auditorias,
    )

    cotizaciones = CotizacionDolarService(
        repositorios["cotizaciones"],
        tipos_cotizacion,
        auditorias,
    )

    return {
        "generos": generos,
        "editoriales": editoriales,
        "monedas": monedas,
        "tipos_cotizacion": tipos_cotizacion,
        "libros": libros,
        "precios": precios,
        "stock": stock,
        "cotizaciones": cotizaciones,
        "auditorias": auditorias,
    }


def main(import_default_data: bool = True) -> None:
    """Ejecuta el sistema Book Manager."""
    conexion = ConexionDB()
    try:
        if import_default_data:
            repositorios = cargar_datos_iniciales(conexion)
        else:
            repositorios = crear_repositorios(conexion)

        iniciar_menu(crear_servicios(repositorios))
    finally:
        conexion.cerrar()


if __name__ == "__main__":
    main()
