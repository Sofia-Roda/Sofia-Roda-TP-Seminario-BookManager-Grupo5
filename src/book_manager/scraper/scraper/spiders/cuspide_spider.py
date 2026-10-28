"""Spider encargado de obtener información de libros desde Cúspide."""
import json
import re
import unicodedata
from urllib.parse import urlencode

import scrapy

from scraper.items import CuspideItem
from scraper.loaders import CuspideItemLoader


class CuspideSpider(scrapy.Spider):
    """Busca en Cúspide únicamente los libros del catálogo de Book Manager."""

    name = "cuspide"

    allowed_domains = [
        "cuspide.com",
        "www.cuspide.com",
    ]

    def __init__(
        self,
        titulos: str = "",
        *args,
        **kwargs,
    ) -> None:
        """Recibe separados por punto y coma los títulos que se deben buscar."""
        super().__init__(*args, **kwargs)

        self.titulos = [
            titulo.strip()
            for titulo in titulos.split(";")
            if titulo.strip()
        ]
        
    async def start(self):
        """Genera una búsqueda en Cúspide por cada título recibido."""
        for titulo in self.titulos:
            parametros = urlencode(
                {
                    "s": titulo,
                    "post_type": "product",
                }
            )

            url = f"https://cuspide.com/?{parametros}"

            yield scrapy.Request(
                url=url,
                callback=self.parse_busqueda,
                cb_kwargs={"titulo_buscado": titulo},
            )
                
    def parse_busqueda(
        self,
        response: scrapy.http.Response,
        titulo_buscado: str,
    ):
        """Procesa como máximo los primeros diez resultados encontrados."""
        enlaces = response.xpath(
            "//a[contains(@href, '/producto/')]/@href"
        ).getall()

        # Evita repetir enlaces conservando el orden original.
        enlaces = list(dict.fromkeys(enlaces))

        print(
            f"Búsqueda: {titulo_buscado} - "
            f"Resultados encontrados: {len(enlaces)}"
        )

        for enlace in enlaces[:10]:
            yield response.follow(
                enlace,
                callback=self.parse_libro,
                cb_kwargs={"titulo_buscado": titulo_buscado},
            )
            
    def parse_libro(
        self,
        response: scrapy.http.Response,
        titulo_buscado: str,
    ):
        """Extrae los datos requeridos desde la ficha de un libro."""
        titulo_encontrado = response.css(
            "h1.product_title::text"
        ).get()

        if not titulo_encontrado:
            return

        if not self._es_mismo_titulo(
            titulo_buscado,
            titulo_encontrado,
        ):
            return

        precio = response.css(
            ".summary .price "
            ".woocommerce-Price-amount bdi::text"
        ).get()

        if precio is None:
            precio = " ".join(
                response.css(
                    ".summary .price ::text"
                ).getall()
            )

        datos_json = response.xpath(
            "//script[@type='application/ld+json']/text()"
        ).get()

        imagen_url = None
        producto = None
        
        if datos_json:
            datos = json.loads(datos_json)

            producto = next(
                (
                    elemento
                    for elemento in datos.get("@graph", [])
                    if elemento.get("@type") == "Product"
                ),
                None,
            )

            if producto is not None:
                sku = producto.get("sku")

                if sku:
                    imagen_url = response.css(
                        f"img[src*='{sku}']::attr(src)"
                    ).get()

        descripcion = response.xpath(
            "//*[normalize-space(text())='Descripción']"
            "/parent::*/following-sibling::*[1]//text()"
        ).getall()

        descripcion = [
            texto.strip()
            for texto in descripcion
            if texto.strip()
        ]

        if producto is not None:
            sku = producto.get("sku")

            if descripcion == [sku]:
                descripcion = []

        formas_pago = response.xpath(
            "//*[contains("
            "normalize-space(.), "
            "'Para compras dentro de la Argentina, "
            "las formas de pago son:'"
            ")]/following::ul[1]/li//text()"
        ).getall()
        formas_pago = [
            forma.strip().lstrip(">").strip()
            for forma in formas_pago
            if forma.strip()
        ]

        formas_pago = list(dict.fromkeys(formas_pago))

        loader = CuspideItemLoader(
            item=CuspideItem(),
            response=response,
        )

        loader.add_value(
            "titulo_buscado",
            titulo_buscado,
        )

        loader.add_value(
            "titulo_encontrado",
            titulo_encontrado,
        )

        loader.add_value(
            "precio",
            precio,
        )

        loader.add_value(
            "imagen_url",
            imagen_url or "No informada",
        )

        loader.add_value(
            "formas_pago",
            formas_pago or ["No informadas"],
        )

        loader.add_value(
            "descripcion",
            descripcion or ["No informada"],
        )

        loader.add_value(
            "url",
            response.url,
        )

        yield loader.load_item()

    @staticmethod
    def _normalizar_titulo(titulo: str) -> str:
        """Normaliza un título para poder compararlo con otro."""
        titulo = titulo.lower()

        titulo = unicodedata.normalize(
            "NFKD",
            titulo,
        )

        titulo = "".join(
            caracter
            for caracter in titulo
            if not unicodedata.combining(caracter)
        )

        titulo = re.sub(
            r"[^a-z0-9]+",
            " ",
            titulo,
        )

        return " ".join(titulo.split())

    @classmethod
    def _es_mismo_titulo(
        cls,
        titulo_buscado: str,
        titulo_encontrado: str,
    ) -> bool:
        """Comprueba si el resultado corresponde al libro buscado."""
        buscado = cls._normalizar_titulo(titulo_buscado)
        encontrado = cls._normalizar_titulo(titulo_encontrado)

        return buscado == encontrado