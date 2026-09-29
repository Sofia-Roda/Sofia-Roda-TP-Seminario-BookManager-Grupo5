from book_manager.preload_data.preload_data import (
    cargar_datos_iniciales,
    crear_repositorios,
)
from book_manager.ui.console import iniciar_menu


def main(import_default_data: bool = True) -> None:
    """Ejecuta el sistema Book Manager."""
    if import_default_data:
        repositorios = cargar_datos_iniciales()
    else:
        repositorios = crear_repositorios()

    iniciar_menu(repositorios)


if __name__ == "__main__":
    main()