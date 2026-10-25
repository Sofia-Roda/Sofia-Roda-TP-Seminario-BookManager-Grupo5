# Changelog

## Sprint 3

[Ejercicio 1]
- Se creó la rama Sprint_3 a partir de Sprint_2.
- Se generó la carpeta scraper con la estructura del proyecto Scrapy mediante scrapy startproject (scrapy.cfg, items.py, middlewares.py, pipelines.py, settings.py y spiders/).
- Se agregó la carpeta reportes para almacenar los reportes Excel generados.
- Se agregó scrapy a requirements.txt.
- Se actualizó el README.md con el objetivo, la introducción y el contexto del Sprint 3.
- Se corrigió en el CHANGELOG del Sprint 2 [Ejercicio 2] la descripción de la conexión: si no está definida DATABASE_URL se lanza un ValueError (no se usa SQLite por defecto).

## Sprint 2

[Ejercicio 8]
- Se agregó la opción de menú para obtener las cotizaciones del dólar mediante la API.
- Se agregó la visualización bimonetaria de precios en ARS y USD utilizando el tipo de cotización seleccionado.
- Se agregó la exportación de los precios registrados a un archivo CSV, incluyendo la moneda asociada a cada precio.
- Se integraron las nuevas opciones dentro de los menús de Precios y Cotizaciones del dólar.

[Ejercicio 7]
- Se corrigió la actualización de fechas en LibroService usando establecer_fechas.
- Se corrigió la ruta del archivo .env (RUTA_ENV) para que funcione tanto en Colab como en entorno local.
- Se agregó un error claro cuando no se encuentra API_URL.
- Se agregaron requests y python-dotenv a requirements.txt.
- Se agregó la equivalencia de nombres de la API (Bolsa = MEP, Contado con liquidación = CCL) para registrar todas las cotizaciones.
- Se creó el archivo .env con la URL de la API del dólar.
- Se agregaron los imports de requests, dotenv y os al servicio.
- Se implementó el método obtener_cotizaciones() en CotizacionDolarService.
- El método consulta la API dolarapi.com, busca el tipo de cotización correspondiente y guarda cada cotización en la base de datos.
- Se evita duplicar cotizaciones ya registradas para la misma fecha y tipo.

[Ejercicio 6]
- Se adaptó preload_data.py para crear las tablas, cargar los datos de migrations/sql cuando la base está vacía y crear los repositorios con ConexionDB.
- Se adaptó main.py para crear la conexión a la base de datos, usarla en todo el sistema y cerrarla al finalizar.
- Se agregó una verificación del sistema completo con los datos precargados.
- Se reescribieron los repositorios para usar SQLAlchemy y base de datos en lugar de CSV.
- Se implementó RepositorioGenero con CRUD completo usando base de datos.
- Se implementó RepositorioEditorial con CRUD completo usando base de datos.
- Se implementó RepositorioMoneda con CRUD completo usando base de datos.
- Se implementó RepositorioTipoCotizacion con CRUD completo usando base de datos.
- Se implementó RepositorioLibro con CRUD completo usando base de datos.
- Se implementó RepositorioPrecio con CRUD completo usando base de datos.
- Se implementó RepositorioStock con CRUD completo usando base de datos.
- Se implementó RepositorioCotizacionDolar con CRUD completo usando base de datos.

[Ejercicio 5]
- Se creó el módulo migrations/migrations.py con la función migrar_datos(carpeta_csvs, carpeta_sqls) para migrar los datos de los CSV del TP1 a SQL.
- Se definió el orden de migración (generos, editoriales, monedas, tipos_cotizacion, libros, precios, stock, cotizaciones_dolar) para respetar las dependencias de claves foráneas.
- Se agregó la función auxiliar _generar_inserts, que lee cada CSV con csv.DictReader y genera las sentencias INSERT INTO.
- Se agregó la función auxiliar _formatear_valor: los valores vacíos pasan a NULL, las columnas numéricas se insertan sin comillas y las comillas simples de los textos se escapan.
- Se generó un archivo .sql por tabla en migrations/sql, con un comentario de encabezado.
- Se agregó la creación automática de la carpeta de destino y un FileNotFoundError si falta algún CSV.
- Se agregó un mensaje por consola con la cantidad de filas generadas por tabla.

[Ejercicio 4]
- Se definieron los modelos ORM del sistema con SQLAlchemy (GeneroModel, EditorialModel, MonedaModel, TipoCotizacionModel, LibroModel, PrecioModel, StockModel, CotizacionDolarModel).
- Se crearon las tablas correspondientes a las entidades del sistema.
- Se establecieron claves foráneas y relaciones entre los modelos con relationship() y back_populates.
- Se agregó la restricción de unicidad tipo_cotizacion_id + fecha en cotizaciones_dolar.

[Ejercicio 3]
- Se agregó el context manager transaccion a la clase ConexionDB en database/connection.py.
- Se confirman los cambios (commit) cuando el bloque termina sin errores.
- Se deshacen los cambios (rollback) y se relanza la excepción cuando ocurre un error.
- Se cierra la sesión siempre al finalizar el bloque.

[Ejercicio 2]
- Se creó la clase ConexionDB en database/connection.py para manejar la conexión con SQLAlchemy.
- Se configuró la URL de conexión a partir de la variable DATABASE_URL del archivo .env (Supabase/PostgreSQL); si no está definida, se lanza un ValueError.
- Se configuró la fábrica de sesiones con expire_on_commit=False.
- Se agregaron métodos para crear sesiones, probar la conexión y cerrarla.
- Se agregaron SQLAlchemy y psycopg[binary] a requirements.txt y se ignoraron los archivos .db.

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
