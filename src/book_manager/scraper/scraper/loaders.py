"""Contiene los loaders utilizados para limpiar los datos del scraper."""

import re
from typing import Optional

from itemloaders import ItemLoader
from itemloaders.processors import Identity, Join, MapCompose, TakeFirst


def limpiar_texto(valor: str) -> Optional[str]:
    """Elimina espacios innecesarios de un texto."""
    texto = " ".join(valor.split())

    if not texto:
        return None

    return texto


def limpiar_precio(valor: str) -> Optional[float]:
    """Convierte un precio expresado como texto a un número decimal."""
    texto = valor.replace("\xa0", " ")

    coincidencia = re.search(
        r"\d[\d.]*,\d{2}",
        texto,
    )

    if coincidencia is None:
        return None

    precio = coincidencia.group()
    precio = precio.replace(".", "")
    precio = precio.replace(",", ".")

    return float(precio)


class CuspideItemLoader(ItemLoader):
    """Limpia y organiza los datos extraídos desde Cúspide."""

    default_input_processor = MapCompose(limpiar_texto)
    default_output_processor = TakeFirst()

    precio_in = MapCompose(limpiar_precio)

    formas_pago_out = Identity()

    descripcion_out = Join(" ")