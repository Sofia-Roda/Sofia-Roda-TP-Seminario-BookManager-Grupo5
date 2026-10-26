"""Contiene las validaciones aplicadas a los datos extraídos."""

from scrapy.exceptions import DropItem


class CuspidePipeline:
    """Valida los libros extraídos y evita resultados duplicados."""

    def __init__(self) -> None:
        self._urls_procesadas: set[str] = set()

    def process_item(self, item):
        """Valida un ítem antes de continuar su procesamiento."""
        if not item.get("titulo_encontrado"):
            raise DropItem("El libro no tiene título.")

        if item.get("precio") is None:
            raise DropItem(
                f"El libro {item['titulo_encontrado']} no tiene precio."
            )

        if item["precio"] <= 0:
            raise DropItem(
                f"El libro {item['titulo_encontrado']} tiene un precio inválido."
            )

        url = item.get("url")

        if not url:
            raise DropItem("El libro no tiene URL.")

        if url in self._urls_procesadas:
            raise DropItem(f"Libro duplicado: {url}")

        self._urls_procesadas.add(url)

        return item