
import abc
import datetime
from typing import Generic, List, Optional, TypeVar

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
            tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
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


class RepositorioGenerico(IRepositorio[T]):
    """Repositorio genérico en memoria, basado en una lista, para entidades de tipo T."""

    def __init__(self) -> None:
        self._elementos: List[T] = []

    def crear(self, entidad: T) -> T:
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe una entidad con id {entidad.id}.")
        self._elementos.append(entidad)
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        for elemento in self._elementos:
            if elemento.id == id:
                return elemento
        return None

    def leer_todos(self) -> List[T]:
        return list(self._elementos)

    def actualizar(self, entidad: T) -> T:
        for indice, elemento in enumerate(self._elementos):
            if elemento.id == entidad.id:
                self._elementos[indice] = entidad
                return entidad
        raise ValueError(f"No se encontró la entidad con id {entidad.id} para actualizar.")

    def eliminar(self, id: int) -> bool:
        for indice, elemento in enumerate(self._elementos):
            if elemento.id == id:
                del self._elementos[indice]
                return True
        return False


class RepositorioGenero(RepositorioGenerico[Genero]):
    """Repositorio para la entidad Genero."""


class RepositorioEditorial(RepositorioGenerico[Editorial]):
    """Repositorio para la entidad Editorial."""


class RepositorioMoneda(RepositorioGenerico[Moneda]):
    """Repositorio para la entidad Moneda."""


class RepositorioTipoCotizacion(RepositorioGenerico[TipoCotizacion]):
    """Repositorio para la entidad TipoCotizacion."""


class RepositorioLibro(RepositorioGenerico[Libro]):
    """Repositorio para la entidad Libro."""


class RepositorioPrecio(RepositorioGenerico[Precio]):
    """Repositorio para la entidad Precio."""


class RepositorioStock(IRepositorioStock):
    """Repositorio en memoria para la entidad Stock, indexado por el id del libro."""

    def __init__(self) -> None:
        self._elementos: List[Stock] = []

    def crear(self, stock: Stock) -> Stock:
        if self.leer_por_libro(stock.libro.id) is not None:
            raise ValueError(f"Ya existe stock para el libro con id {stock.libro.id}.")
        self._elementos.append(stock)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        for elemento in self._elementos:
            if elemento.libro.id == libro_id:
                return elemento
        return None

    def actualizar(self, stock: Stock) -> Stock:
        for indice, elemento in enumerate(self._elementos):
            if elemento.libro.id == stock.libro.id:
                self._elementos[indice] = stock
                return stock
        raise ValueError(f"No se encontró stock para el libro con id {stock.libro.id} para actualizar.")

    def eliminar(self, libro_id: int) -> bool:
        for indice, elemento in enumerate(self._elementos):
            if elemento.libro.id == libro_id:
                del self._elementos[indice]
                return True
        return False


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """Repositorio en memoria para la entidad CotizacionDolar, indexado por tipo y fecha."""

    def __init__(self) -> None:
        self._elementos: List[CotizacionDolar] = []

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        if self.leer_por_tipo_y_fecha(cotizacion.tipo_cotizacion.id, cotizacion.fecha) is not None:
            raise ValueError("Ya existe una cotización para ese tipo y fecha.")
        self._elementos.append(cotizacion)
        return cotizacion

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional[CotizacionDolar]:
        for elemento in self._elementos:
            if elemento.tipo_cotizacion.id == tipo_id and elemento.fecha == fecha:
                return elemento
        return None

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        return [elemento for elemento in self._elementos if elemento.tipo_cotizacion.id == tipo_id]

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        for indice, elemento in enumerate(self._elementos):
            if (elemento.tipo_cotizacion.id == cotizacion.tipo_cotizacion.id
                    and elemento.fecha == cotizacion.fecha):
                self._elementos[indice] = cotizacion
                return cotizacion
        raise ValueError("No se encontró la cotización para actualizar.")

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        for indice, elemento in enumerate(self._elementos):
            if elemento.tipo_cotizacion.id == tipo_id and elemento.fecha == fecha:
                del self._elementos[indice]
                return True
        return False
