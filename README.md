# Book Manager - Sprint 3

## Sprint actual: Sprint 3

## Objetivo

Obtener datos de la web mediante técnicas de web scraping con Scrapy para
comparar los precios internos del catálogo del Book Manager con los precios
publicados por la competencia (sitio de Cúspide), generando alertas,
reportes en Excel y un registro de auditoría de las operaciones del sistema.

## Introducción y contexto

En el Sprint 1 se desarrolló el sistema Book Manager utilizando entidades,
repositorios y archivos CSV para la carga y persistencia inicial de los datos.

En el Sprint 2 el sistema evolucionó hacia el uso de una base de datos
relacional con SQLAlchemy, se migraron los datos desde los archivos CSV y se
incorporó el consumo de una API externa para obtener cotizaciones del dólar.

En este Sprint 3, partiendo de la última entrega del Sprint 2, se descargarán
y obtendrán datos de la web para trabajar con ellos. La idea es obtener los
precios de nuestros competidores (librerías con venta online) para poder
compararnos con ellos y competir de forma más informada.

Para ello se implementará un scraper (CuspideSpider) con Scrapy que buscará
en el sitio de Cúspide únicamente los libros de nuestro catálogo, obteniendo
precio, imagen, formas de pago y descripción detallada. Con esos datos se
compararán los precios internos con los precios web, se generarán alertas en
CSV y reportes en Excel, y se auditarán todas las operaciones del sistema.
