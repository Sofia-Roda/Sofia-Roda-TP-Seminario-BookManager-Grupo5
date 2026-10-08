from typing import Dict

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


def crear_servicios(repositorios: Dict[str, object]) -> Dict[str, object]:
    """Instancia los servicios de negocio a partir de los repositorios."""
    generos = GeneroService(repositorios["generos"], repositorios["libros"])
    editoriales = EditorialService(
        repositorios["editoriales"], repositorios["libros"]
    )
    monedas = MonedaService(repositorios["monedas"])
    tipos_cotizacion = TipoCotizacionService(repositorios["tipos_cotizacion"])
    libros = LibroService(repositorios["libros"], generos, editoriales)

    return {
        "generos": generos,
        "editoriales": editoriales,
        "monedas": monedas,
        "tipos_cotizacion": tipos_cotizacion,
        "libros": libros,
        "precios": PrecioService(repositorios["precios"], libros, monedas),
        "stock": StockService(repositorios["stock"], libros),
        "cotizaciones": CotizacionDolarService(
            repositorios["cotizaciones"], tipos_cotizacion
        ),
    }


def main(import_default_data: bool = True) -> None:
    """Ejecuta el sistema Book Manager."""
    if import_default_data:
        repositorios = cargar_datos_iniciales()
    else:
        repositorios = crear_repositorios()

    iniciar_menu(crear_servicios(repositorios))


if __name__ == "__main__":
    main()
