
import datetime
from typing import List, Optional

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    EntidadBase,
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


def _siguiente_id(entidades: List[EntidadBase]) -> int:
    """Calcula el próximo id disponible a partir de los ids ya utilizados."""
    return max((entidad.id for entidad in entidades), default=0) + 1


class GeneroService:
    """Lógica de negocio para la gestión de géneros literarios."""

    def __init__(self, repositorio: RepositorioGenero) -> None:
        self._repositorio = repositorio

    def crear(self, nombre: str, descripcion: Optional[str] = None) -> Genero:
        """Valida los datos y crea un nuevo género.

        Raises:
            ValueError: Si el nombre está vacío.
        """
        self._validar_nombre(nombre)
        genero = Genero(id=_siguiente_id(self._repositorio.leer_todos()),
                         nombre=nombre, descripcion=descripcion)
        return self._repositorio.crear(genero)

    def obtener_por_id(self, id: int) -> Optional[Genero]:
        """Obtiene un género por su id, o None si no existe."""
        return self._repositorio.leer_por_id(id)

    def listar(self) -> List[Genero]:
        """Devuelve todos los géneros registrados."""
        return self._repositorio.leer_todos()

    def actualizar(self, id: int, nombre: Optional[str] = None,
                   descripcion: Optional[str] = None) -> Genero:
        """Actualiza los datos de un género existente.

        Raises:
            ValueError: Si no existe un género con ese id, o si el nuevo
                nombre está vacío.
        """
        genero = self._repositorio.leer_por_id(id)
        if genero is None:
            raise ValueError(f"No existe un género con id {id}.")
        if nombre is not None:
            self._validar_nombre(nombre)
            genero.nombre = nombre
        if descripcion is not None:
            genero.descripcion = descripcion
        return self._repositorio.actualizar(genero)

    def eliminar(self, id: int) -> bool:
        """Elimina un género por su id. Devuelve True si existía."""
        return self._repositorio.eliminar(id)

    @staticmethod
    def _validar_nombre(nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del género no puede estar vacío.")


class EditorialService:
    """Lógica de negocio para la gestión de editoriales."""

    def __init__(self, repositorio: RepositorioEditorial) -> None:
        self._repositorio = repositorio

    def crear(self, nombre: str, cuit: str, email: str, telefono: str,
              pais: str) -> Editorial:
        """Valida los datos y crea una nueva editorial.

        Raises:
            ValueError: Si algún dato obligatorio es inválido.
        """
        self._validar_nombre(nombre)
        self._validar_cuit(cuit)
        self._validar_email(email)
        editorial = Editorial(id=_siguiente_id(self._repositorio.leer_todos()),
                               nombre=nombre, cuit=cuit, email=email,
                               telefono=telefono, pais=pais)
        return self._repositorio.crear(editorial)

    def obtener_por_id(self, id: int) -> Optional[Editorial]:
        """Obtiene una editorial por su id, o None si no existe."""
        return self._repositorio.leer_por_id(id)

    def listar(self) -> List[Editorial]:
        """Devuelve todas las editoriales registradas."""
        return self._repositorio.leer_todos()

    def actualizar(self, id: int, nombre: Optional[str] = None,
                   cuit: Optional[str] = None, email: Optional[str] = None,
                   telefono: Optional[str] = None,
                   pais: Optional[str] = None) -> Editorial:
        """Actualiza los datos de una editorial existente.

        Raises:
            ValueError: Si no existe la editorial, o si algún dato nuevo
                es inválido.
        """
        editorial = self._repositorio.leer_por_id(id)
        if editorial is None:
            raise ValueError(f"No existe una editorial con id {id}.")
        if nombre is not None:
            self._validar_nombre(nombre)
            editorial.nombre = nombre
        if cuit is not None:
            self._validar_cuit(cuit)
            editorial.cuit = cuit
        if email is not None:
            self._validar_email(email)
            editorial.email = email
        if telefono is not None:
            editorial.telefono = telefono
        if pais is not None:
            editorial.pais = pais
        return self._repositorio.actualizar(editorial)

    def eliminar(self, id: int) -> bool:
        """Elimina una editorial por su id. Devuelve True si existía."""
        return self._repositorio.eliminar(id)

    @staticmethod
    def _validar_nombre(nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la editorial no puede estar vacío.")

    @staticmethod
    def _validar_cuit(cuit: str) -> None:
        solo_digitos = cuit.replace("-", "")
        if not solo_digitos.isdigit() or len(solo_digitos) != 11:
            raise ValueError(f"CUIT inválido: {cuit}.")

    @staticmethod
    def _validar_email(email: str) -> None:
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError(f"Email inválido: {email}.")


class MonedaService:
    """Lógica de negocio para la gestión de monedas."""

    def __init__(self, repositorio: RepositorioMoneda) -> None:
        self._repositorio = repositorio

    def crear(self, nombre: str, simbolo: str, codigo: str) -> Moneda:
        """Valida los datos y crea una nueva moneda.

        Raises:
            ValueError: Si el nombre está vacío o el código no tiene el
                formato ISO 4217 (3 letras).
        """
        self._validar_nombre(nombre)
        codigo_normalizado = self._validar_codigo(codigo)
        moneda = Moneda(id=_siguiente_id(self._repositorio.leer_todos()),
                         nombre=nombre, simbolo=simbolo,
                         codigo=codigo_normalizado)
        return self._repositorio.crear(moneda)

    def obtener_por_id(self, id: int) -> Optional[Moneda]:
        """Obtiene una moneda por su id, o None si no existe."""
        return self._repositorio.leer_por_id(id)

    def listar(self) -> List[Moneda]:
        """Devuelve todas las monedas registradas."""
        return self._repositorio.leer_todos()

    def actualizar(self, id: int, nombre: Optional[str] = None,
                   simbolo: Optional[str] = None,
                   codigo: Optional[str] = None) -> Moneda:
        """Actualiza los datos de una moneda existente.

        Raises:
            ValueError: Si no existe la moneda, o si el nuevo código es
                inválido.
        """
        moneda = self._repositorio.leer_por_id(id)
        if moneda is None:
            raise ValueError(f"No existe una moneda con id {id}.")
        if nombre is not None:
            self._validar_nombre(nombre)
            moneda.nombre = nombre
        if simbolo is not None:
            moneda.simbolo = simbolo
        if codigo is not None:
            moneda.codigo = self._validar_codigo(codigo)
        return self._repositorio.actualizar(moneda)

    def eliminar(self, id: int) -> bool:
        """Elimina una moneda por su id. Devuelve True si existía."""
        return self._repositorio.eliminar(id)

    @staticmethod
    def _validar_nombre(nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la moneda no puede estar vacío.")

    @staticmethod
    def _validar_codigo(codigo: str) -> str:
        if not codigo.isalpha() or len(codigo) != 3:
            raise ValueError(f"Código de moneda inválido: {codigo}.")
        return codigo.upper()


class TipoCotizacionService:
    """Lógica de negocio para la gestión de tipos de cotización."""

    def __init__(self, repositorio: RepositorioTipoCotizacion) -> None:
        self._repositorio = repositorio

    def crear(self, nombre: str,
              descripcion: Optional[str] = None) -> TipoCotizacion:
        """Valida los datos y crea un nuevo tipo de cotización.

        Raises:
            ValueError: Si el nombre está vacío.
        """
        self._validar_nombre(nombre)
        tipo = TipoCotizacion(id=_siguiente_id(self._repositorio.leer_todos()),
                               nombre=nombre, descripcion=descripcion)
        return self._repositorio.crear(tipo)

    def obtener_por_id(self, id: int) -> Optional[TipoCotizacion]:
        """Obtiene un tipo de cotización por su id, o None si no existe."""
        return self._repositorio.leer_por_id(id)

    def listar(self) -> List[TipoCotizacion]:
        """Devuelve todos los tipos de cotización registrados."""
        return self._repositorio.leer_todos()

    def actualizar(self, id: int, nombre: Optional[str] = None,
                   descripcion: Optional[str] = None) -> TipoCotizacion:
        """Actualiza los datos de un tipo de cotización existente.

        Raises:
            ValueError: Si no existe, o si el nuevo nombre está vacío.
        """
        tipo = self._repositorio.leer_por_id(id)
        if tipo is None:
            raise ValueError(f"No existe un tipo de cotización con id {id}.")
        if nombre is not None:
            self._validar_nombre(nombre)
            tipo.nombre = nombre
        if descripcion is not None:
            tipo.descripcion = descripcion
        return self._repositorio.actualizar(tipo)

    def eliminar(self, id: int) -> bool:
        """Elimina un tipo de cotización por su id. Devuelve True si existía."""
        return self._repositorio.eliminar(id)

    @staticmethod
    def _validar_nombre(nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError(
                "El nombre del tipo de cotización no puede estar vacío."
            )


class LibroService:
    """Lógica de negocio para la gestión del catálogo de libros."""

    def __init__(self, repositorio: RepositorioLibro,
                 genero_service: GeneroService,
                 editorial_service: EditorialService) -> None:
        self._repositorio = repositorio
        self._genero_service = genero_service
        self._editorial_service = editorial_service

    def crear(self, isbn: str, titulo: str, autor: str, genero_id: int,
              editorial_id: int, idioma: str,
              fecha_publicacion: datetime.date,
              fecha_primera_publicacion: datetime.date,
              num_paginas: int, peso: float,
              descripcion: Optional[str] = None,
              ranking: Optional[int] = None) -> Libro:
        """Valida los datos y da de alta un nuevo libro en el catálogo.

        Raises:
            ValueError: Si algún dato es inválido, o si el género o la
                editorial indicados no existen.
        """
        genero = self._obtener_genero_o_error(genero_id)
        editorial = self._obtener_editorial_o_error(editorial_id)
        self._validar_isbn(isbn)
        self._validar_texto(titulo, "título")
        self._validar_texto(autor, "autor")
        self._validar_texto(idioma, "idioma")
        self._validar_fechas(fecha_publicacion, fecha_primera_publicacion)
        self._validar_num_paginas(num_paginas)
        self._validar_peso(peso)
        libro = Libro(id=_siguiente_id(self._repositorio.leer_todos()),
                      isbn=isbn, titulo=titulo, autor=autor, genero=genero,
                      editorial=editorial, idioma=idioma,
                      fecha_publicacion=fecha_publicacion,
                      fecha_primera_publicacion=fecha_primera_publicacion,
                      num_paginas=num_paginas, peso=peso,
                      descripcion=descripcion, ranking=ranking)
        return self._repositorio.crear(libro)

    def obtener_por_id(self, id: int) -> Optional[Libro]:
        """Obtiene un libro por su id, o None si no existe."""
        return self._repositorio.leer_por_id(id)

    def listar(self) -> List[Libro]:
        """Devuelve todos los libros del catálogo."""
        return self._repositorio.leer_todos()

    def actualizar(self, id: int, isbn: Optional[str] = None,
                   titulo: Optional[str] = None, autor: Optional[str] = None,
                   genero_id: Optional[int] = None,
                   editorial_id: Optional[int] = None,
                   idioma: Optional[str] = None,
                   fecha_publicacion: Optional[datetime.date] = None,
                   fecha_primera_publicacion: Optional[datetime.date] = None,
                   num_paginas: Optional[int] = None,
                   peso: Optional[float] = None,
                   descripcion: Optional[str] = None,
                   ranking: Optional[int] = None) -> Libro:
        """Actualiza los datos de un libro existente.

        Raises:
            ValueError: Si no existe el libro, o si algún dato nuevo es
                inválido.
        """
        libro = self._repositorio.leer_por_id(id)
        if libro is None:
            raise ValueError(f"No existe un libro con id {id}.")

        # Se valida la coherencia entre ambas fechas antes de mutar el
        # libro: como el repositorio guarda la misma referencia en
        # memoria, escribir un campo antes de validar el par dejaría el
        # objeto en un estado inconsistente si la validación falla.
        nueva_fecha_publicacion = fecha_publicacion or libro.fecha_publicacion
        nueva_fecha_primera = (fecha_primera_publicacion
                                or libro.fecha_primera_publicacion)
        self._validar_fechas(nueva_fecha_publicacion, nueva_fecha_primera)

        if isbn is not None:
            self._validar_isbn(isbn)
            libro.isbn = isbn
        if titulo is not None:
            self._validar_texto(titulo, "título")
            libro.titulo = titulo
        if autor is not None:
            self._validar_texto(autor, "autor")
            libro.autor = autor
        if genero_id is not None:
            libro.genero = self._obtener_genero_o_error(genero_id)
        if editorial_id is not None:
            libro.editorial = self._obtener_editorial_o_error(editorial_id)
        if idioma is not None:
            self._validar_texto(idioma, "idioma")
            libro.idioma = idioma
        libro.fecha_publicacion = nueva_fecha_publicacion
        libro.fecha_primera_publicacion = nueva_fecha_primera
        if num_paginas is not None:
            self._validar_num_paginas(num_paginas)
            libro.num_paginas = num_paginas
        if peso is not None:
            self._validar_peso(peso)
            libro.peso = peso
        if descripcion is not None:
            libro.descripcion = descripcion
        if ranking is not None:
            libro.ranking = ranking
        return self._repositorio.actualizar(libro)

    def eliminar(self, id: int) -> bool:
        """Elimina un libro por su id. Devuelve True si existía."""
        return self._repositorio.eliminar(id)

    def _obtener_genero_o_error(self, genero_id: int) -> Genero:
        genero = self._genero_service.obtener_por_id(genero_id)
        if genero is None:
            raise ValueError(f"No existe un género con id {genero_id}.")
        return genero

    def _obtener_editorial_o_error(self, editorial_id: int) -> Editorial:
        editorial = self._editorial_service.obtener_por_id(editorial_id)
        if editorial is None:
            raise ValueError(
                f"No existe una editorial con id {editorial_id}."
            )
        return editorial

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> None:
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacío.")

    @staticmethod
    def _validar_isbn(isbn: str) -> None:
        solo_digitos = isbn.replace("-", "")
        if not solo_digitos.isdigit() or len(solo_digitos) not in (10, 13):
            raise ValueError(f"ISBN inválido: {isbn}.")

    @staticmethod
    def _validar_fechas(fecha_publicacion: datetime.date,
                         fecha_primera_publicacion: datetime.date) -> None:
        if fecha_primera_publicacion > fecha_publicacion:
            raise ValueError(
                "La fecha de primera publicación no puede ser posterior "
                "a la fecha de publicación."
            )

    @staticmethod
    def _validar_num_paginas(num_paginas: int) -> None:
        if num_paginas <= 0:
            raise ValueError("El número de páginas debe ser mayor a cero.")

    @staticmethod
    def _validar_peso(peso: float) -> None:
        if peso <= 0:
            raise ValueError("El peso del libro debe ser mayor a cero.")


class PrecioService:
    """Lógica de negocio para la gestión de precios de libros."""

    def __init__(self, repositorio: RepositorioPrecio,
                 libro_service: LibroService,
                 moneda_service: MonedaService) -> None:
        self._repositorio = repositorio
        self._libro_service = libro_service
        self._moneda_service = moneda_service

    def crear(self, libro_id: int, moneda_id: int, valor: float) -> Precio:
        """Valida los datos y da de alta un nuevo precio para un libro.

        Raises:
            ValueError: Si el libro o la moneda no existen, o si el valor
                no es mayor a cero.
        """
        libro = self._obtener_libro_o_error(libro_id)
        moneda = self._obtener_moneda_o_error(moneda_id)
        self._validar_valor(valor)
        precio = Precio(id=_siguiente_id(self._repositorio.leer_todos()),
                         libro=libro, moneda=moneda, valor=valor)
        return self._repositorio.crear(precio)

    def obtener_por_id(self, id: int) -> Optional[Precio]:
        """Obtiene un precio por su id, o None si no existe."""
        return self._repositorio.leer_por_id(id)

    def listar(self) -> List[Precio]:
        """Devuelve todos los precios registrados."""
        return self._repositorio.leer_todos()

    def actualizar(self, id: int, moneda_id: Optional[int] = None,
                   valor: Optional[float] = None) -> Precio:
        """Actualiza los datos de un precio existente.

        Raises:
            ValueError: Si no existe el precio, si la nueva moneda no
                existe, o si el nuevo valor no es mayor a cero.
        """
        precio = self._repositorio.leer_por_id(id)
        if precio is None:
            raise ValueError(f"No existe un precio con id {id}.")
        if moneda_id is not None:
            precio.moneda = self._obtener_moneda_o_error(moneda_id)
        if valor is not None:
            self._validar_valor(valor)
            precio.valor = valor
        return self._repositorio.actualizar(precio)

    def eliminar(self, id: int) -> bool:
        """Elimina un precio por su id. Devuelve True si existía."""
        return self._repositorio.eliminar(id)

    def _obtener_libro_o_error(self, libro_id: int) -> Libro:
        libro = self._libro_service.obtener_por_id(libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con id {libro_id}.")
        return libro

    def _obtener_moneda_o_error(self, moneda_id: int) -> Moneda:
        moneda = self._moneda_service.obtener_por_id(moneda_id)
        if moneda is None:
            raise ValueError(f"No existe una moneda con id {moneda_id}.")
        return moneda

    @staticmethod
    def _validar_valor(valor: float) -> None:
        if valor <= 0:
            raise ValueError("El valor del precio debe ser mayor a cero.")


class StockService:
    """Lógica de negocio para la gestión del stock de libros."""

    ESTADOS_VALIDOS = frozenset(
        {"disponible", "agotado", "reservado", "descatalogado"}
    )

    def __init__(self, repositorio: RepositorioStock,
                 libro_service: LibroService) -> None:
        self._repositorio = repositorio
        self._libro_service = libro_service

    def crear(self, libro_id: int, cantidad: int, estado: str,
              ubicacion: str, fecha_ingreso: datetime.date) -> Stock:
        """Valida los datos y registra el stock inicial de un libro.

        Raises:
            ValueError: Si el libro no existe, la cantidad es negativa,
                o el estado no es uno de los estados válidos.
        """
        libro = self._obtener_libro_o_error(libro_id)
        self._validar_cantidad(cantidad)
        self._validar_estado(estado)
        # El stock es 1 a 1 con el libro y el repositorio indexa por
        # libro_id (no por id propio): se reutiliza el id del libro para
        # no necesitar un segundo generador de ids independiente.
        stock = Stock(id=libro.id, libro=libro, cantidad=cantidad,
                       estado=estado, ubicacion=ubicacion,
                       fecha_ingreso=fecha_ingreso)
        return self._repositorio.crear(stock)

    def obtener_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Obtiene el stock de un libro, o None si no tiene stock registrado."""
        return self._repositorio.leer_por_libro(libro_id)

    def actualizar(self, libro_id: int, cantidad: Optional[int] = None,
                   estado: Optional[str] = None,
                   ubicacion: Optional[str] = None,
                   fecha_ingreso: Optional[datetime.date] = None) -> Stock:
        """Actualiza el stock existente de un libro.

        Raises:
            ValueError: Si no hay stock registrado para el libro, o si
                algún dato nuevo es inválido.
        """
        stock = self._repositorio.leer_por_libro(libro_id)
        if stock is None:
            raise ValueError(
                f"No existe stock para el libro con id {libro_id}."
            )
        if cantidad is not None:
            self._validar_cantidad(cantidad)
            stock.cantidad = cantidad
        if estado is not None:
            self._validar_estado(estado)
            stock.estado = estado
        if ubicacion is not None:
            stock.ubicacion = ubicacion
        if fecha_ingreso is not None:
            stock.fecha_ingreso = fecha_ingreso
        return self._repositorio.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el stock de un libro. Devuelve True si existía."""
        return self._repositorio.eliminar(libro_id)

    def _obtener_libro_o_error(self, libro_id: int) -> Libro:
        libro = self._libro_service.obtener_por_id(libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con id {libro_id}.")
        return libro

    @classmethod
    def _validar_cantidad(cls, cantidad: int) -> None:
        if cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")

    @classmethod
    def _validar_estado(cls, estado: str) -> None:
        if estado not in cls.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado de stock inválido: {estado}. "
                f"Valores permitidos: {sorted(cls.ESTADOS_VALIDOS)}."
            )


class CotizacionDolarService:
    """Lógica de negocio para la gestión de cotizaciones del dólar."""

    def __init__(self, repositorio: RepositorioCotizacionDolar,
                 tipo_cotizacion_service: TipoCotizacionService) -> None:
        self._repositorio = repositorio
        self._tipo_cotizacion_service = tipo_cotizacion_service
        self._siguiente_id = 1

    def crear(self, tipo_cotizacion_id: int, fecha: datetime.date,
              valor: float) -> CotizacionDolar:
        """Valida los datos y registra una nueva cotización del dólar.

        Raises:
            ValueError: Si el tipo de cotización no existe, la fecha es
                futura, o el valor no es mayor a cero.
        """
        tipo = self._obtener_tipo_o_error(tipo_cotizacion_id)
        self._validar_valor(valor)
        self._validar_fecha(fecha)
        cotizacion = CotizacionDolar(id=self._generar_id(),
                                      tipo_cotizacion=tipo, fecha=fecha,
                                      valor=valor)
        return self._repositorio.crear(cotizacion)

    def obtener_por_tipo_y_fecha(
        self, tipo_cotizacion_id: int, fecha: datetime.date
    ) -> Optional[CotizacionDolar]:
        """Obtiene la cotización de un tipo en una fecha dada, o None."""
        return self._repositorio.leer_por_tipo_y_fecha(tipo_cotizacion_id,
                                                         fecha)

    def listar_historico(self,
                          tipo_cotizacion_id: int) -> List[CotizacionDolar]:
        """Devuelve el histórico de cotizaciones de un tipo dado."""
        return self._repositorio.leer_historico_por_tipo(tipo_cotizacion_id)

    def actualizar(self, tipo_cotizacion_id: int, fecha: datetime.date,
                   valor: float) -> CotizacionDolar:
        """Actualiza el valor de una cotización existente.

        Raises:
            ValueError: Si no existe la cotización, o el nuevo valor no
                es mayor a cero.
        """
        cotizacion = self._repositorio.leer_por_tipo_y_fecha(
            tipo_cotizacion_id, fecha
        )
        if cotizacion is None:
            raise ValueError("No existe una cotización para ese tipo y fecha.")
        self._validar_valor(valor)
        cotizacion.valor = valor
        return self._repositorio.actualizar(cotizacion)

    def eliminar(self, tipo_cotizacion_id: int, fecha: datetime.date) -> bool:
        """Elimina la cotización de un tipo en una fecha.

        Devuelve True si existía.
        """
        return self._repositorio.eliminar(tipo_cotizacion_id, fecha)

    def _obtener_tipo_o_error(self,
                              tipo_cotizacion_id: int) -> TipoCotizacion:
        tipo = self._tipo_cotizacion_service.obtener_por_id(
            tipo_cotizacion_id
        )
        if tipo is None:
            raise ValueError(
                f"No existe un tipo de cotización con id {tipo_cotizacion_id}."
            )
        return tipo

    def _generar_id(self) -> int:
        # El repositorio de cotizaciones indexa por (tipo, fecha), no por
        # id propio, por lo que se mantiene un contador interno para
        # asignar un id único a cada alta.
        id_generado = self._siguiente_id
        self._siguiente_id += 1
        return id_generado

    @staticmethod
    def _validar_valor(valor: float) -> None:
        if valor <= 0:
            raise ValueError("El valor de la cotización debe ser mayor a cero.")

    @staticmethod
    def _validar_fecha(fecha: datetime.date) -> None:
        if fecha > datetime.date.today():
            raise ValueError("La fecha de la cotización no puede ser futura.")
