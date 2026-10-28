
"""Contiene los repositorios encargados del acceso a la base de datos."""
import abc
import datetime
from typing import Generic, List, Optional, TypeVar

from sqlalchemy import select

from book_manager.database.connection import ConexionDB
from book_manager.entities.entities import (
    Auditoria,
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
from book_manager.models.models import (
    AuditoriaModel,
    CotizacionDolarModel,
    EditorialModel,
    GeneroModel,
    LibroModel,
    MonedaModel,
    PrecioModel,
    StockModel,
    TipoCotizacionModel,
)

T = TypeVar('T', bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad en el repositorio.

        Args:
            entidad (T): La entidad a crear.

        Returns:
            T: La entidad creada.

        Raises:
            ValueError: Si ya existe una entidad con el mismo ID.
        """
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a leer.

        Returns:
            Optional[T]: La entidad si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades del repositorio.

        Returns:
            List[T]: Una lista de todas las entidades.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente en el repositorio.

        Args:
            entidad (T): La entidad a actualizar (debe tener un ID existente).

        Returns:
            T: La entidad actualizada.

        Raises:
            ValueError: Si no se encuentra la entidad para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a eliminar.

        Returns:
            bool: True si la entidad fue eliminada, False si no se encontró.
        """
        pass


class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock.

        Args:
            stock (Stock): El objeto Stock a crear.

        Returns:
            Stock: El objeto Stock creado.

        Raises:
            ValueError: Si ya existe un registro de stock para el mismo libro.
        """
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional['Stock']:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, stock: 'Stock') -> 'Stock':
        """Actualiza un registro de stock existente.

        Args:
            stock (Stock): El objeto Stock a actualizar (debe tener un libro_id existente).

        Returns:
            Stock: El objeto Stock actualizado.

        Raises:
            ValueError: Si no se encuentra el stock para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass


class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

    @abc.abstractmethod
    def crear(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
        """Crea una nueva cotización de dólar.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar creado.

        Raises:
            ValueError: Si ya existe una cotización para el mismo tipo y fecha.
        """
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional['CotizacionDolar']:
        """Lee una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (datetime.date): La fecha de la cotización.

        Returns:
            Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List['CotizacionDolar']:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar actualizado.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (datetime.date): La fecha de la cotización a eliminar.

        Returns:
            bool: True si la cotización fue eliminada, False si no se encontró.
        """
        pass


class RepositorioGenero(IRepositorio[Genero]):
    """Repositorio para la entidad Genero usando base de datos."""

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def crear(self, entidad: Genero) -> Genero:
        """Guarda un nuevo género en la base de datos."""
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe un género con id {entidad.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = GeneroModel(
                id=entidad.id,
                nombre=entidad.nombre,
                descripcion=entidad.descripcion,
            )
            sesion.add(modelo)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Genero]:
        """Obtiene un género por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(GeneroModel, id)
            if modelo is None:
                return None
            return Genero(
                id=modelo.id,
                nombre=modelo.nombre,
                descripcion=modelo.descripcion,
            )

    def leer_todos(self) -> List[Genero]:
        """Devuelve todos los géneros registrados."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(select(GeneroModel)).scalars().all()
            return [
                Genero(id=m.id, nombre=m.nombre, descripcion=m.descripcion)
                for m in modelos
            ]

    def actualizar(self, entidad: Genero) -> Genero:
        """Actualiza los datos de un género existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(GeneroModel, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encontró el género con id {entidad.id}.")
            modelo.nombre = entidad.nombre
            modelo.descripcion = entidad.descripcion
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina un género por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(GeneroModel, id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioEditorial(IRepositorio[Editorial]):
    """Repositorio para la entidad Editorial usando base de datos."""

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def crear(self, entidad: Editorial) -> Editorial:
        """Crea una nueva editorial en la base de datos."""
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe una editorial con id {entidad.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = EditorialModel(
                id=entidad.id,
                nombre=entidad.nombre,
                cuit=entidad.cuit,
                email=entidad.email,
                telefono=entidad.telefono,
                pais=entidad.pais,
            )
            sesion.add(modelo)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Editorial]:
        """Obtiene una editorial por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(EditorialModel, id)
            if modelo is None:
                return None
            return Editorial(
                id=modelo.id,
                nombre=modelo.nombre,
                cuit=modelo.cuit,
                email=modelo.email,
                telefono=modelo.telefono,
                pais=modelo.pais,
            )

    def leer_todos(self) -> List[Editorial]:
        """Devuelve todas las editoriales registradas."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(select(EditorialModel)).scalars().all()
            return [
                Editorial(
                    id=m.id, nombre=m.nombre, cuit=m.cuit,
                    email=m.email, telefono=m.telefono, pais=m.pais,
                )
                for m in modelos
            ]

    def actualizar(self, entidad: Editorial) -> Editorial:
        """Actualiza los datos de una editorial existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(EditorialModel, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encontró la editorial con id {entidad.id}.")
            modelo.nombre = entidad.nombre
            modelo.cuit = entidad.cuit
            modelo.email = entidad.email
            modelo.telefono = entidad.telefono
            modelo.pais = entidad.pais
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina una editorial por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(EditorialModel, id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioMoneda(IRepositorio[Moneda]):
    """Repositorio para la entidad Moneda usando base de datos."""

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def crear(self, entidad: Moneda) -> Moneda:
        """Guarda una nueva moneda en la base de datos."""
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe una moneda con id {entidad.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = MonedaModel(
                id=entidad.id,
                nombre=entidad.nombre,
                simbolo=entidad.simbolo,
                codigo=entidad.codigo,
            )
            sesion.add(modelo)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        """Devuelve una moneda por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(MonedaModel, id)
            if modelo is None:
                return None
            return Moneda(
                id=modelo.id,
                nombre=modelo.nombre,
                simbolo=modelo.simbolo,
                codigo=modelo.codigo,
            )

    def leer_todos(self) -> List[Moneda]:
        """Devuelve todas las monedas registradas."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(select(MonedaModel)).scalars().all()
            return [
                Moneda(id=m.id, nombre=m.nombre, simbolo=m.simbolo, codigo=m.codigo)
                for m in modelos
            ]

    def actualizar(self, entidad: Moneda) -> Moneda:
        """Actualiza los datos de una moneda existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(MonedaModel, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encontró la moneda con id {entidad.id}.")
            modelo.nombre = entidad.nombre
            modelo.simbolo = entidad.simbolo
            modelo.codigo = entidad.codigo
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina una moneda por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(MonedaModel, id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioTipoCotizacion(IRepositorio[TipoCotizacion]):
    """Repositorio para la entidad TipoCotizacion usando base de datos."""

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def crear(self, entidad: TipoCotizacion) -> TipoCotizacion:
        """Guarda un nuevo tipo de cotización en la base de datos."""
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe un tipo de cotización con id {entidad.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = TipoCotizacionModel(
                id=entidad.id,
                nombre=entidad.nombre,
                descripcion=entidad.descripcion,
            )
            sesion.add(modelo)
        return entidad

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        """Devuelve un tipo de cotización por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(TipoCotizacionModel, id)
            if modelo is None:
                return None
            return TipoCotizacion(
                id=modelo.id,
                nombre=modelo.nombre,
                descripcion=modelo.descripcion,
            )

    def leer_todos(self) -> List[TipoCotizacion]:
        """Devuelve todos los tipos de cotización registrados."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(select(TipoCotizacionModel)).scalars().all()
            return [
                TipoCotizacion(id=m.id, nombre=m.nombre, descripcion=m.descripcion)
                for m in modelos
            ]

    def actualizar(self, entidad: TipoCotizacion) -> TipoCotizacion:
        """Actualiza los datos de un tipo de cotización existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(TipoCotizacionModel, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encontró el tipo de cotización con id {entidad.id}.")
            modelo.nombre = entidad.nombre
            modelo.descripcion = entidad.descripcion
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina un tipo de cotización por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(TipoCotizacionModel, id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioLibro(IRepositorio[Libro]):
    """Repositorio para la entidad Libro usando base de datos."""

    def __init__(self, conexion: ConexionDB,
                 repositorio_generos: RepositorioGenero,
                 repositorio_editoriales: RepositorioEditorial) -> None:
        self._conexion = conexion
        self._repositorio_generos = repositorio_generos
        self._repositorio_editoriales = repositorio_editoriales

    def _modelo_a_entidad(self, modelo: LibroModel) -> Libro:
        """Convierte un modelo de base de datos en una entidad Libro."""
        return Libro(
            id=modelo.id,
            isbn=modelo.isbn,
            titulo=modelo.titulo,
            autor=modelo.autor,
            genero=self._repositorio_generos.leer_por_id(modelo.genero_id),
            editorial=self._repositorio_editoriales.leer_por_id(modelo.editorial_id),
            idioma=modelo.idioma,
            fecha_publicacion=modelo.fecha_publicacion,
            fecha_primera_publicacion=modelo.fecha_primera_publicacion,
            num_paginas=modelo.num_paginas,
            peso=modelo.peso,
            descripcion=modelo.descripcion,
            ranking=modelo.ranking,
        )

    def crear(self, entidad: Libro) -> Libro:
        """Guarda un nuevo libro en la base de datos."""
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe un libro con id {entidad.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = LibroModel(
                id=entidad.id,
                isbn=entidad.isbn,
                titulo=entidad.titulo,
                autor=entidad.autor,
                genero_id=entidad.genero.id,
                editorial_id=entidad.editorial.id,
                idioma=entidad.idioma,
                fecha_publicacion=entidad.fecha_publicacion,
                fecha_primera_publicacion=entidad.fecha_primera_publicacion,
                num_paginas=entidad.num_paginas,
                peso=entidad.peso,
                descripcion=entidad.descripcion,
                ranking=entidad.ranking,
            )
            sesion.add(modelo)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Libro]:
        """Devuelve un libro por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(LibroModel, id)
            if modelo is None:
                return None
            return self._modelo_a_entidad(modelo)

    def leer_todos(self) -> List[Libro]:
        """Devuelve todos los libros registrados."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(select(LibroModel)).scalars().all()
            return [self._modelo_a_entidad(m) for m in modelos]

    def actualizar(self, entidad: Libro) -> Libro:
        """Actualiza los datos de un libro existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(LibroModel, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encontró el libro con id {entidad.id}.")
            modelo.isbn = entidad.isbn
            modelo.titulo = entidad.titulo
            modelo.autor = entidad.autor
            modelo.genero_id = entidad.genero.id
            modelo.editorial_id = entidad.editorial.id
            modelo.idioma = entidad.idioma
            modelo.fecha_publicacion = entidad.fecha_publicacion
            modelo.fecha_primera_publicacion = entidad.fecha_primera_publicacion
            modelo.num_paginas = entidad.num_paginas
            modelo.peso = entidad.peso
            modelo.descripcion = entidad.descripcion
            modelo.ranking = entidad.ranking
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina un libro por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(LibroModel, id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioPrecio(IRepositorio[Precio]):
    """Repositorio para la entidad Precio usando base de datos."""

    def __init__(self, conexion: ConexionDB,
                 repositorio_libros: RepositorioLibro,
                 repositorio_monedas: RepositorioMoneda) -> None:
        self._conexion = conexion
        self._repositorio_libros = repositorio_libros
        self._repositorio_monedas = repositorio_monedas

    def _modelo_a_entidad(self, modelo: PrecioModel) -> Precio:
        """Convierte un modelo de base de datos en una entidad Precio."""
        return Precio(
            id=modelo.id,
            libro=self._repositorio_libros.leer_por_id(modelo.libro_id),
            moneda=self._repositorio_monedas.leer_por_id(modelo.moneda_id),
            valor=modelo.valor,
        )

    def crear(self, entidad: Precio) -> Precio:
        """Guarda un nuevo precio en la base de datos."""
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe un precio con id {entidad.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = PrecioModel(
                id=entidad.id,
                libro_id=entidad.libro.id,
                moneda_id=entidad.moneda.id,
                valor=entidad.valor,
            )
            sesion.add(modelo)
        return entidad

    def leer_por_id(self, id: int) -> Optional[Precio]:
        """Devuelve un precio por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(PrecioModel, id)
            if modelo is None:
                return None
            return self._modelo_a_entidad(modelo)

    def leer_todos(self) -> List[Precio]:
        """Devuelve todos los precios registrados."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(select(PrecioModel)).scalars().all()
            return [self._modelo_a_entidad(m) for m in modelos]

    def actualizar(self, entidad: Precio) -> Precio:
        """Actualiza los datos de un precio existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(PrecioModel, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encontró el precio con id {entidad.id}.")
            modelo.libro_id = entidad.libro.id
            modelo.moneda_id = entidad.moneda.id
            modelo.valor = entidad.valor
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina un precio por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(PrecioModel, id)
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioStock(IRepositorioStock):
    """Repositorio para la entidad Stock usando base de datos."""

    def __init__(self, conexion: ConexionDB,
                 repositorio_libros: RepositorioLibro) -> None:
        self._conexion = conexion
        self._repositorio_libros = repositorio_libros

    def _modelo_a_entidad(self, modelo: StockModel) -> Stock:
        """Convierte un modelo de base de datos en una entidad Stock."""
        return Stock(
            id=modelo.id,
            libro=self._repositorio_libros.leer_por_id(modelo.libro_id),
            cantidad=modelo.cantidad,
            estado=modelo.estado,
            ubicacion=modelo.ubicacion,
            fecha_ingreso=modelo.fecha_ingreso,
        )

    def crear(self, stock: Stock) -> Stock:
        """Guarda un nuevo stock en la base de datos."""
        if self.leer_por_libro(stock.libro.id) is not None:
            raise ValueError(f"Ya existe stock para el libro con id {stock.libro.id}.")
        with self._conexion.transaccion() as sesion:
            modelo = StockModel(
                id=stock.id,
                libro_id=stock.libro.id,
                cantidad=stock.cantidad,
                estado=stock.estado,
                ubicacion=stock.ubicacion,
                fecha_ingreso=stock.fecha_ingreso,
            )
            sesion.add(modelo)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Devuelve el stock asociado a un libro por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.execute(
                select(StockModel).where(StockModel.libro_id == libro_id)
            ).scalar_one_or_none()
            if modelo is None:
                return None
            return self._modelo_a_entidad(modelo)

    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza los datos de un stock existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.execute(
                select(StockModel).where(StockModel.libro_id == stock.libro.id)
            ).scalar_one_or_none()
            if modelo is None:
                raise ValueError(f"No se encontró stock para el libro con id {stock.libro.id}.")
            modelo.cantidad = stock.cantidad
            modelo.estado = stock.estado
            modelo.ubicacion = stock.ubicacion
            modelo.fecha_ingreso = stock.fecha_ingreso
        return stock

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el stock asociado a un libro por su id."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.execute(
                select(StockModel).where(StockModel.libro_id == libro_id)
            ).scalar_one_or_none()
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """Repositorio para la entidad CotizacionDolar usando base de datos."""

    def __init__(self, conexion: ConexionDB,
                 repositorio_tipos: RepositorioTipoCotizacion) -> None:
        self._conexion = conexion
        self._repositorio_tipos = repositorio_tipos

    def _modelo_a_entidad(self, modelo: CotizacionDolarModel) -> CotizacionDolar:
        """Convierte un modelo de base de datos en una entidad CotizacionDolar."""
        return CotizacionDolar(
            id=modelo.id,
            tipo_cotizacion=self._repositorio_tipos.leer_por_id(modelo.tipo_cotizacion_id),
            fecha=modelo.fecha,
            valor=modelo.valor,
            compra=modelo.compra,
        )

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Guarda una nueva cotización de dólar en la base de datos."""
        if self.leer_por_tipo_y_fecha(cotizacion.tipo_cotizacion.id, cotizacion.fecha) is not None:
            raise ValueError("Ya existe una cotización para ese tipo y fecha.")
        with self._conexion.transaccion() as sesion:
            modelo = CotizacionDolarModel(
                id=cotizacion.id,
                tipo_cotizacion_id=cotizacion.tipo_cotizacion.id,
                fecha=cotizacion.fecha,
                compra=cotizacion.compra,
                valor=cotizacion.valor,
            )
            sesion.add(modelo)
        return cotizacion

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional[CotizacionDolar]:
        """Devuelve una cotización de dólar por tipo y fecha."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.execute(
                select(CotizacionDolarModel).where(
                    CotizacionDolarModel.tipo_cotizacion_id == tipo_id,
                    CotizacionDolarModel.fecha == fecha,
                )
            ).scalar_one_or_none()
            if modelo is None:
                return None
            return self._modelo_a_entidad(modelo)

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        """Devuelve el histórico de cotizaciones para un tipo específico."""
        with self._conexion.transaccion() as sesion:
            modelos = sesion.execute(
                select(CotizacionDolarModel).where(
                    CotizacionDolarModel.tipo_cotizacion_id == tipo_id
                )
            ).scalars().all()
            return [self._modelo_a_entidad(m) for m in modelos]

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.execute(
                select(CotizacionDolarModel).where(
                    CotizacionDolarModel.tipo_cotizacion_id == cotizacion.tipo_cotizacion.id,
                    CotizacionDolarModel.fecha == cotizacion.fecha,
                )
            ).scalar_one_or_none()
            if modelo is None:
                raise ValueError("No se encontró la cotización para actualizar.")
            modelo.compra = cotizacion.compra
            modelo.valor = cotizacion.valor
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina una cotización de dólar por tipo y fecha."""
        with self._conexion.transaccion() as sesion:
            modelo = sesion.execute(
                select(CotizacionDolarModel).where(
                    CotizacionDolarModel.tipo_cotizacion_id == tipo_id,
                    CotizacionDolarModel.fecha == fecha,
                )
            ).scalar_one_or_none()
            if modelo is None:
                return False
            sesion.delete(modelo)
        return True


class RepositorioAuditoria:
    """Repositorio para registrar y consultar las auditorías del sistema."""

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def crear(self, auditoria: Auditoria) -> Auditoria:
        """Guarda un nuevo registro de auditoría en la base de datos."""
        with self._conexion.transaccion() as sesion:
            modelo = AuditoriaModel(
                id=auditoria.id,
                accion=auditoria.accion,
                fecha=auditoria.fecha,
                detalles=auditoria.detalles,
            )
            sesion.add(modelo)

        return auditoria

    def leer_todos(self) -> List[Auditoria]:
        """Devuelve todas las auditorías ordenadas desde la más reciente."""
        with self._conexion.transaccion() as sesion:
            modelos = (
                sesion.execute(
                    select(AuditoriaModel).order_by(
                        AuditoriaModel.fecha.desc(),
                        AuditoriaModel.id.desc(),
                    )
                )
                .scalars()
                .all()
            )

            return [
                Auditoria(
                    id=modelo.id,
                    accion=modelo.accion,
                    fecha=modelo.fecha,
                    detalles=modelo.detalles,
                )
                for modelo in modelos
            ]