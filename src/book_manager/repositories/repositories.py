
import abc
import csv
import datetime
import os
from typing import Dict, Generic, List, Optional, TypeVar

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


class RepositorioCSV(abc.ABC, Generic[T]):
    """Base para repositorios que persisten sus entidades en un archivo CSV.

    Al crearse lee el archivo indicado y, ante cada alta, modificación o
    baja, lo vuelve a escribir completo. Si no se indica archivo, los datos
    solo se mantienen en memoria.
    """

    COLUMNAS: List[str] = []

    def __init__(self, ruta_archivo: Optional[str] = None) -> None:
        self._elementos: List[T] = []
        self._ruta_archivo = ruta_archivo
        self._cargar()

    @abc.abstractmethod
    def _desde_fila(self, fila: Dict[str, str]) -> T:
        """Convierte una fila del CSV en una entidad."""
        pass

    @abc.abstractmethod
    def _a_fila(self, entidad: T) -> Dict[str, object]:
        """Convierte una entidad en una fila del CSV."""
        pass

    def _cargar(self) -> None:
        if self._ruta_archivo is None or not os.path.exists(self._ruta_archivo):
            return
        with open(self._ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                self._elementos.append(self._desde_fila(fila))

    def _guardar(self) -> None:
        if self._ruta_archivo is None:
            return
        # Se escribe primero en un archivo temporal y luego se reemplaza el
        # original, para no dejarlo a medio escribir si algo falla.
        ruta_temporal = self._ruta_archivo + ".tmp"
        with open(ruta_temporal, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=self.COLUMNAS)
            escritor.writeheader()
            for elemento in self._elementos:
                escritor.writerow(self._a_fila(elemento))
        os.replace(ruta_temporal, self._ruta_archivo)


def _texto_opcional(valor: str) -> Optional[str]:
    return valor if valor != "" else None


def _entero_opcional(valor: str) -> Optional[int]:
    return int(valor) if valor != "" else None


def _vacio_si_none(valor: object) -> object:
    return "" if valor is None else valor


class RepositorioGenerico(RepositorioCSV[T], IRepositorio[T]):
    """Repositorio genérico, persistido en CSV, para entidades de tipo T."""

    def crear(self, entidad: T) -> T:
        if self.leer_por_id(entidad.id) is not None:
            raise ValueError(f"Ya existe una entidad con id {entidad.id}.")
        self._elementos.append(entidad)
        self._guardar()
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
                self._guardar()
                return entidad
        raise ValueError(f"No se encontró la entidad con id {entidad.id} para actualizar.")

    def eliminar(self, id: int) -> bool:
        for indice, elemento in enumerate(self._elementos):
            if elemento.id == id:
                del self._elementos[indice]
                self._guardar()
                return True
        return False


class RepositorioGenero(RepositorioGenerico[Genero]):
    """Repositorio para la entidad Genero."""

    COLUMNAS = ["id", "nombre", "descripcion"]

    def _desde_fila(self, fila: Dict[str, str]) -> Genero:
        return Genero(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            descripcion=_texto_opcional(fila["descripcion"]),
        )

    def _a_fila(self, genero: Genero) -> Dict[str, object]:
        return {
            "id": genero.id,
            "nombre": genero.nombre,
            "descripcion": _vacio_si_none(genero.descripcion),
        }


class RepositorioEditorial(RepositorioGenerico[Editorial]):
    """Repositorio para la entidad Editorial."""

    COLUMNAS = ["id", "nombre", "cuit", "email", "telefono", "pais"]

    def _desde_fila(self, fila: Dict[str, str]) -> Editorial:
        return Editorial(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            cuit=fila["cuit"],
            email=fila["email"],
            telefono=fila["telefono"],
            pais=fila["pais"],
        )

    def _a_fila(self, editorial: Editorial) -> Dict[str, object]:
        return {
            "id": editorial.id,
            "nombre": editorial.nombre,
            "cuit": editorial.cuit,
            "email": editorial.email,
            "telefono": editorial.telefono,
            "pais": editorial.pais,
        }


class RepositorioMoneda(RepositorioGenerico[Moneda]):
    """Repositorio para la entidad Moneda."""

    COLUMNAS = ["id", "nombre", "simbolo", "codigo"]

    def _desde_fila(self, fila: Dict[str, str]) -> Moneda:
        return Moneda(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            simbolo=fila["simbolo"],
            codigo=fila["codigo"],
        )

    def _a_fila(self, moneda: Moneda) -> Dict[str, object]:
        return {
            "id": moneda.id,
            "nombre": moneda.nombre,
            "simbolo": moneda.simbolo,
            "codigo": moneda.codigo,
        }


class RepositorioTipoCotizacion(RepositorioGenerico[TipoCotizacion]):
    """Repositorio para la entidad TipoCotizacion."""

    COLUMNAS = ["id", "nombre", "descripcion"]

    def _desde_fila(self, fila: Dict[str, str]) -> TipoCotizacion:
        return TipoCotizacion(
            id=int(fila["id"]),
            nombre=fila["nombre"],
            descripcion=_texto_opcional(fila["descripcion"]),
        )

    def _a_fila(self, tipo: TipoCotizacion) -> Dict[str, object]:
        return {
            "id": tipo.id,
            "nombre": tipo.nombre,
            "descripcion": _vacio_si_none(tipo.descripcion),
        }


def _buscar_relacionado(repositorio: IRepositorio, id: int, archivo: str, campo: str):
    """Obtiene la entidad relacionada a una fila, o falla si no existe."""
    entidad = repositorio.leer_por_id(id)
    if entidad is None:
        raise ValueError(f"{archivo}: no existe {campo} con id {id}.")
    return entidad


class RepositorioLibro(RepositorioGenerico[Libro]):
    """Repositorio para la entidad Libro.

    En el archivo se guardan los ids de género y editorial; al leerlo se
    obtienen las entidades desde sus repositorios.
    """

    COLUMNAS = ["id", "isbn", "titulo", "autor", "genero_id", "editorial_id",
                "idioma", "fecha_publicacion", "fecha_primera_publicacion",
                "num_paginas", "peso", "descripcion", "ranking"]

    def __init__(self, repositorio_generos: RepositorioGenero,
                 repositorio_editoriales: RepositorioEditorial,
                 ruta_archivo: Optional[str] = None) -> None:
        self._repositorio_generos = repositorio_generos
        self._repositorio_editoriales = repositorio_editoriales
        super().__init__(ruta_archivo)

    def _desde_fila(self, fila: Dict[str, str]) -> Libro:
        return Libro(
            id=int(fila["id"]),
            isbn=fila["isbn"],
            titulo=fila["titulo"],
            autor=fila["autor"],
            genero=_buscar_relacionado(self._repositorio_generos,
                                       int(fila["genero_id"]),
                                       "libros.csv", "el género"),
            editorial=_buscar_relacionado(self._repositorio_editoriales,
                                          int(fila["editorial_id"]),
                                          "libros.csv", "la editorial"),
            idioma=fila["idioma"],
            fecha_publicacion=datetime.date.fromisoformat(
                fila["fecha_publicacion"]
            ),
            fecha_primera_publicacion=datetime.date.fromisoformat(
                fila["fecha_primera_publicacion"]
            ),
            num_paginas=int(fila["num_paginas"]),
            peso=float(fila["peso"]),
            descripcion=_texto_opcional(fila["descripcion"]),
            ranking=_entero_opcional(fila["ranking"]),
        )

    def _a_fila(self, libro: Libro) -> Dict[str, object]:
        return {
            "id": libro.id,
            "isbn": libro.isbn,
            "titulo": libro.titulo,
            "autor": libro.autor,
            "genero_id": libro.genero.id,
            "editorial_id": libro.editorial.id,
            "idioma": libro.idioma,
            "fecha_publicacion": libro.fecha_publicacion.isoformat(),
            "fecha_primera_publicacion": libro.fecha_primera_publicacion.isoformat(),
            "num_paginas": libro.num_paginas,
            "peso": libro.peso,
            "descripcion": _vacio_si_none(libro.descripcion),
            "ranking": _vacio_si_none(libro.ranking),
        }


class RepositorioPrecio(RepositorioGenerico[Precio]):
    """Repositorio para la entidad Precio (guarda los ids de libro y moneda)."""

    COLUMNAS = ["id", "libro_id", "moneda_id", "valor"]

    def __init__(self, repositorio_libros: RepositorioLibro,
                 repositorio_monedas: RepositorioMoneda,
                 ruta_archivo: Optional[str] = None) -> None:
        self._repositorio_libros = repositorio_libros
        self._repositorio_monedas = repositorio_monedas
        super().__init__(ruta_archivo)

    def _desde_fila(self, fila: Dict[str, str]) -> Precio:
        return Precio(
            id=int(fila["id"]),
            libro=_buscar_relacionado(self._repositorio_libros,
                                      int(fila["libro_id"]),
                                      "precios.csv", "el libro"),
            moneda=_buscar_relacionado(self._repositorio_monedas,
                                       int(fila["moneda_id"]),
                                       "precios.csv", "la moneda"),
            valor=float(fila["valor"]),
        )

    def _a_fila(self, precio: Precio) -> Dict[str, object]:
        return {
            "id": precio.id,
            "libro_id": precio.libro.id,
            "moneda_id": precio.moneda.id,
            "valor": precio.valor,
        }


class RepositorioStock(RepositorioCSV[Stock], IRepositorioStock):
    """Repositorio para la entidad Stock, indexado por el id del libro y persistido en CSV."""

    COLUMNAS = ["id", "libro_id", "cantidad", "estado", "ubicacion",
                "fecha_ingreso"]

    def __init__(self, repositorio_libros: RepositorioLibro,
                 ruta_archivo: Optional[str] = None) -> None:
        self._repositorio_libros = repositorio_libros
        super().__init__(ruta_archivo)

    def _desde_fila(self, fila: Dict[str, str]) -> Stock:
        return Stock(
            id=int(fila["id"]),
            libro=_buscar_relacionado(self._repositorio_libros,
                                      int(fila["libro_id"]),
                                      "stock.csv", "el libro"),
            cantidad=int(fila["cantidad"]),
            estado=fila["estado"],
            ubicacion=fila["ubicacion"],
            fecha_ingreso=datetime.date.fromisoformat(fila["fecha_ingreso"]),
        )

    def _a_fila(self, stock: Stock) -> Dict[str, object]:
        return {
            "id": stock.id,
            "libro_id": stock.libro.id,
            "cantidad": stock.cantidad,
            "estado": stock.estado,
            "ubicacion": stock.ubicacion,
            "fecha_ingreso": stock.fecha_ingreso.isoformat(),
        }

    def crear(self, stock: Stock) -> Stock:
        if self.leer_por_libro(stock.libro.id) is not None:
            raise ValueError(f"Ya existe stock para el libro con id {stock.libro.id}.")
        self._elementos.append(stock)
        self._guardar()
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
                self._guardar()
                return stock
        raise ValueError(f"No se encontró stock para el libro con id {stock.libro.id} para actualizar.")

    def eliminar(self, libro_id: int) -> bool:
        for indice, elemento in enumerate(self._elementos):
            if elemento.libro.id == libro_id:
                del self._elementos[indice]
                self._guardar()
                return True
        return False


class RepositorioCotizacionDolar(RepositorioCSV[CotizacionDolar], IRepositorioCotizacionDolar):
    """Repositorio para la entidad CotizacionDolar, indexado por tipo y fecha y persistido en CSV."""

    COLUMNAS = ["id", "tipo_cotizacion_id", "fecha", "valor"]

    def __init__(self, repositorio_tipos: RepositorioTipoCotizacion,
                 ruta_archivo: Optional[str] = None) -> None:
        self._repositorio_tipos = repositorio_tipos
        super().__init__(ruta_archivo)

    def _desde_fila(self, fila: Dict[str, str]) -> CotizacionDolar:
        return CotizacionDolar(
            id=int(fila["id"]),
            tipo_cotizacion=_buscar_relacionado(self._repositorio_tipos,
                                                int(fila["tipo_cotizacion_id"]),
                                                "cotizaciones_dolar.csv",
                                                "el tipo de cotización"),
            fecha=datetime.date.fromisoformat(fila["fecha"]),
            valor=float(fila["valor"]),
        )

    def _a_fila(self, cotizacion: CotizacionDolar) -> Dict[str, object]:
        return {
            "id": cotizacion.id,
            "tipo_cotizacion_id": cotizacion.tipo_cotizacion.id,
            "fecha": cotizacion.fecha.isoformat(),
            "valor": cotizacion.valor,
        }

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        if self.leer_por_tipo_y_fecha(cotizacion.tipo_cotizacion.id, cotizacion.fecha) is not None:
            raise ValueError("Ya existe una cotización para ese tipo y fecha.")
        self._elementos.append(cotizacion)
        self._guardar()
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
                self._guardar()
                return cotizacion
        raise ValueError("No se encontró la cotización para actualizar.")

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        for indice, elemento in enumerate(self._elementos):
            if elemento.tipo_cotizacion.id == tipo_id and elemento.fecha == fecha:
                del self._elementos[indice]
                self._guardar()
                return True
        return False
