"""Define los datos extraídos desde el sitio web de Cúspide."""

import scrapy


class CuspideItem(scrapy.Item):
    """Representa los datos de un libro obtenidos desde Cúspide."""

    titulo_buscado = scrapy.Field()
    titulo_encontrado = scrapy.Field()
    precio = scrapy.Field()
    imagen_url = scrapy.Field()
    formas_pago = scrapy.Field()
    descripcion = scrapy.Field()
    url = scrapy.Field()