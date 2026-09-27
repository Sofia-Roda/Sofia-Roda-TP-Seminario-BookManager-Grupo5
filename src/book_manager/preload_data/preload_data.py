import csv
import datetime
from typing import Dict, List

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
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


RUTA_CSV = "book_manager/migrations/csv/"


def leer_csv(nombre_archivo: str) -> List[Dict[str, str]]:
    """Lee un archivo CSV y devuelve sus filas."""
    archivo = open(
        RUTA_CSV + nombre_archivo,
        "r",
        encoding="utf-8",
        newline="",
    )
    lector = csv.DictReader(archivo)
    filas = list(lector)
    archivo.close()
    return filas


def convertir_fecha(fecha: str) -> datetime.date:
    """Convierte una fecha AAAA-MM-DD en datetime.date."""
    partes = fecha.split("-")
    return datetime.date(
        int(partes[0]),
        int(partes[1]),
        int(partes[2]),
    )


def crear_repositorios() -> Dict[str, object]:
    """Crea los repositorios necesarios para la aplicación."""
    return {
        "generos": RepositorioGenero(),
        "editoriales": RepositorioEditorial(),
        "monedas": RepositorioMoneda(),
        "tipos_cotizacion": RepositorioTipoCotizacion(),
        "libros": RepositorioLibro(),
        "precios": RepositorioPrecio(),
        "stock": RepositorioStock(),
        "cotizaciones": RepositorioCotizacionDolar(),
    }


def cargar_generos(repositorio: RepositorioGenero) -> None:
    """Carga los géneros desde generos.csv."""
    filas = leer_csv("generos.csv")

    for fila in filas:
        genero = Genero(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
        )
        repositorio.crear(genero)


def cargar_editoriales(repositorio: RepositorioEditorial) -> None:
    """Carga las editoriales desde editoriales.csv."""
    filas = leer_csv("editoriales.csv")

    for fila in filas:
        editorial = Editorial(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            cuit=fila["cuit"],
            email=fila["email"],
            telefono=fila["telefono"],
            pais=fila["pais"],
        )
        repositorio.crear(editorial)


def cargar_monedas(repositorio: RepositorioMoneda) -> None:
    """Carga las monedas desde monedas.csv."""
    filas = leer_csv("monedas.csv")

    for fila in filas:
        moneda = Moneda(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            simbolo=fila["simbolo"],
            codigo=fila["codigo"],
        )
        repositorio.crear(moneda)


def cargar_tipos_cotizacion(
    repositorio: RepositorioTipoCotizacion,
) -> None:
    """Carga los tipos de cotización desde tipos_cotizacion.csv."""
    filas = leer_csv("tipos_cotizacion.csv")

    for fila in filas:
        tipo = TipoCotizacion(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
        )
        repositorio.crear(tipo)


def cargar_libros(
    repositorio: RepositorioLibro,
    repositorio_genero: RepositorioGenero,
    repositorio_editorial: RepositorioEditorial,
) -> None:
    """Carga los libros y relaciona género y editorial."""
    filas = leer_csv("libros.csv")

    for fila in filas:
        genero = repositorio_genero.leer_por_id(
            int(fila["genero_id"])
        )
        editorial = repositorio_editorial.leer_por_id(
            int(fila["editorial_id"])
        )

        libro = Libro(
            id=int(fila["id"]),
            isbn=fila["isbn"],
            titulo=fila["titulo"],
            autor=fila["autor"],
            genero=genero,
            editorial=editorial,
            idioma=fila["idioma"],
            fecha_publicacion=convertir_fecha(
                fila["fecha_publicacion"]
            ),
            fecha_primera_publicacion=convertir_fecha(
                fila["fecha_primera_publicacion"]
            ),
            num_paginas=int(fila["num_paginas"]),
            peso=float(fila["peso"]),
            descripcion=fila["descripcion"],
            ranking=int(fila["ranking"]),
        )
        repositorio.crear(libro)


def cargar_precios(
    repositorio: RepositorioPrecio,
    repositorio_libro: RepositorioLibro,
    repositorio_moneda: RepositorioMoneda,
) -> None:
    """Carga los precios y relaciona libro y moneda."""
    filas = leer_csv("precios.csv")

    for fila in filas:
        libro = repositorio_libro.leer_por_id(
            int(fila["libro_id"])
        )
        moneda = repositorio_moneda.leer_por_id(
            int(fila["moneda_id"])
        )

        precio = Precio(
            id=int(fila["id"]),
            libro=libro,
            moneda=moneda,
            valor=float(fila["valor"]),
        )
        repositorio.crear(precio)


def cargar_stock(
    repositorio: RepositorioStock,
    repositorio_libro: RepositorioLibro,
) -> None:
    """Carga el stock y relaciona cada registro con un libro."""
    filas = leer_csv("stock.csv")

    for fila in filas:
        libro = repositorio_libro.leer_por_id(
            int(fila["libro_id"])
        )

        stock = Stock(
            id=int(fila["id"]),
            libro=libro,
            cantidad=int(fila["cantidad"]),
            estado=fila["estado"],
            ubicacion=fila["ubicacion"],
            fecha_ingreso=convertir_fecha(
                fila["fecha_ingreso"]
            ),
        )
        repositorio.crear(stock)


def cargar_cotizaciones(
    repositorio: RepositorioCotizacionDolar,
    repositorio_tipo: RepositorioTipoCotizacion,
) -> None:
    """Carga las cotizaciones y las relaciona con su tipo."""
    filas = leer_csv("cotizaciones_dolar.csv")

    for fila in filas:
        tipo = repositorio_tipo.leer_por_id(
            int(fila["tipo_cotizacion_id"])
        )

        cotizacion = CotizacionDolar(
            id=int(fila["id"]),
            tipo_cotizacion=tipo,
            fecha=convertir_fecha(fila["fecha"]),
            valor=float(fila["valor"]),
        )
        repositorio.crear(cotizacion)


def cargar_datos_iniciales() -> Dict[str, object]:
    """Crea repositorios y carga todos los datos iniciales."""
    repositorios = crear_repositorios()

    cargar_generos(repositorios["generos"])
    cargar_editoriales(repositorios["editoriales"])
    cargar_monedas(repositorios["monedas"])
    cargar_tipos_cotizacion(
        repositorios["tipos_cotizacion"]
    )
    cargar_libros(
        repositorios["libros"],
        repositorios["generos"],
        repositorios["editoriales"],
    )
    cargar_precios(
        repositorios["precios"],
        repositorios["libros"],
        repositorios["monedas"],
    )
    cargar_stock(
        repositorios["stock"],
        repositorios["libros"],
    )
    cargar_cotizaciones(
        repositorios["cotizaciones"],
        repositorios["tipos_cotizacion"],
    )

    return repositorios
