# Changelog

[Ejercicio 4]
- Definición de clases de servicio (lógica de negocio) para cada entidad:
  GeneroService, EditorialService, MonedaService, TipoCotizacionService,
  LibroService, PrecioService, StockService y CotizacionDolarService
- Generación de ids y validaciones de datos antes de crear/actualizar
  cada entidad (nombres, CUIT, email, código de moneda, ISBN, fechas,
  valores numéricos y estados de stock)
- Validación de existencia de entidades relacionadas (género, editorial,
  libro, moneda, tipo de cotización) al crear o actualizar

[Ejercicio 2]
- Definición de clase base EntidadBase
- Definición de clase Genero con encapsulamiento
- Definición de clase Editorial con encapsulamiento
- Definición de clase Moneda con encapsulamiento
- Definición de clase TipoCotizacion con encapsulamiento
- Definición de clase Libro con relaciones a Genero y Editorial
- Definición de clase Precio con relaciones a Libro y Moneda
- Definición de clase Stock con relaciones a Libro
- Definición de clase CotizacionDolar con relaciones a TipoCotizacion

[Ejercicio 1]
- Inicialización del repositorio en GitHub
- Creación de la rama Sprint_1
- Generación de la estructura de directorios del proyecto
- Creación de archivos base: README.md, CHANGELOG.md, requirements.txt
