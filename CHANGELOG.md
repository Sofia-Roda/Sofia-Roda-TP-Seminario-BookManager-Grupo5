# Changelog

## Sprint 2

[Ejercicio 3]
- Se agregó el context manager transaccion a la clase ConexionDB en database/connection.py.
- Se confirman los cambios (commit) cuando el bloque termina sin errores.
- Se deshacen los cambios (rollback) y se relanza la excepción cuando ocurre un error.
- Se cierra la sesión siempre al finalizar el bloque.

[Ejercicio 2]
- Se creó la clase ConexionDB en database/connection.py para manejar la conexión con SQLAlchemy.
- Se configuró SQLite como base por defecto (book_manager.db en la raíz del proyecto), con la URL de conexión configurable.
- Se activó la validación de claves foráneas en SQLite.
- Se configuró la fábrica de sesiones con expire_on_commit=False.
- Se agregaron métodos para crear sesiones, probar la conexión y cerrarla.
- Se agregó SQLAlchemy a requirements.txt y se ignoraron los archivos .db.

[Ejercicio 1]
- Se creó la rama Sprint_2 a partir de Sprint_1.
- Se incorporó la estructura necesaria para trabajar con base de datos.
- Se agregaron los módulos database y models.
- Se agregó la carpeta migrations/sql para almacenar las sentencias SQL generadas.
- Se preparó la estructura inicial del proyecto para el Sprint 2.

## Sprint 1

[Ejercicio 7]
- Se creó main.py como punto de entrada del sistema.
- Se integró la creación y precarga de repositorios con la interfaz de consola.
- Se agregó la opción import_default_data para ejecutar el sistema con o sin datos precargados.

[Ejercicio 6]
- Se implementó la interfaz de consola del sistema.
- Se agregaron menús CRUD para Género, Editorial, Moneda, TipoCotizacion, Libro, Precio, Stock y CotizacionDolar.
- Se agregaron validaciones para números enteros, decimales y fechas ingresadas por el usuario.
- Se conectó la interfaz de consola con los repositorios del sistema.
- Se realizaron ajustes internos en la interfaz de consola para mejorar la organización, legibilidad y consistencia del código.

[Ejercicio 5]
- Se crearon los archivos CSV para la importación de datos.
- Se agregaron 10 registros para cada entidad.
- Se implementó la precarga de datos desde archivos CSV.
- Se relacionaron los datos precargados con las entidades del sistema.

[Ejercicio 4]
- Se definieron las clases de servicio (lógica de negocio) para cada entidad: GeneroService, EditorialService, MonedaService, TipoCotizacionService, LibroService, PrecioService, StockService y CotizacionDolarService.
- Se agregó la generación de ids y la validación de datos antes de crear o actualizar cada entidad (nombres, CUIT, email, código de moneda, ISBN, fechas, valores numéricos y estados de stock).
- Se agregó la validación de existencia de entidades relacionadas (género, editorial, libro, moneda, tipo de cotización) al crear o actualizar.

[Ejercicio 3]
- Se definió la interfaz genérica IRepositorio para las operaciones CRUD.
- Se implementó RepositorioGenerico basado en listas.
- Se implementaron los repositorios para Género, Editorial, Moneda, TipoCotizacion, Libro y Precio.
- Se implementaron repositorios específicos para Stock y CotizacionDolar.

[Ejercicio 2]
- Se definió la clase base EntidadBase.
- Se definieron las clases Genero, Editorial, Moneda y TipoCotizacion con encapsulamiento.
- Se definió la clase Libro con relaciones a Genero y Editorial.
- Se definió la clase Precio con relaciones a Libro y Moneda.
- Se definió la clase Stock con relación a Libro.
- Se definió la clase CotizacionDolar con relación a TipoCotizacion.

[Ejercicio 1]
- Se inicializó el repositorio en GitHub.
- Se creó la rama Sprint_1.
- Se generó la estructura de directorios del proyecto.
- Se crearon los archivos base: README.md, CHANGELOG.md y requirements.txt.
