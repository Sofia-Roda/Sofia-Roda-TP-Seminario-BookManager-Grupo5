
import datetime
from typing import Optional


class EntidadBase:
    """Clase base para todas las entidades del sistema."""

    def __init__(self, id: int) -> None:
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        self._id = valor

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"


class Genero(EntidadBase):
    """Representa una categoría literaria de un libro."""

    def __init__(self, id: int, nombre: str, descripcion: Optional[str] = None) -> None:
        super().__init__(id)
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: Optional[str]) -> None:
        self._descripcion = valor

    def __repr__(self) -> str:
        return f"Genero(id={self._id}, nombre={self._nombre})"

class Editorial(EntidadBase):
    """Representa una editorial proveedora de libros."""

    def __init__(self, id: int, nombre: str, cuit: str, email: str,
                 telefono: str, pais: str) -> None:
        super().__init__(id)
        self._nombre = nombre
        self._cuit = cuit
        self._email = email
        self._telefono = telefono
        self._pais = pais

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor

    @property
    def cuit(self) -> str:
        return self._cuit

    @cuit.setter
    def cuit(self, valor: str) -> None:
        self._cuit = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = valor

    @property
    def pais(self) -> str:
        return self._pais

    @pais.setter
    def pais(self, valor: str) -> None:
        self._pais = valor

    def __repr__(self) -> str:
        return f"Editorial(id={self._id}, nombre={self._nombre}, pais={self._pais})"

class Moneda(EntidadBase):
    """Representa un tipo de moneda utilizada en el sistema."""

    def __init__(self, id: int, nombre: str, simbolo: str, codigo: str) -> None:
        super().__init__(id)
        self._nombre = nombre
        self._simbolo = simbolo
        self._codigo = codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        self._simbolo = valor

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self._codigo = valor

    def __repr__(self) -> str:
        return f"Moneda(id={self._id}, nombre={self._nombre}, codigo={self._codigo})"

class TipoCotizacion(EntidadBase):
    """Representa un tipo de cotización del dólar (Oficial, Blue, MEP, etc.)."""

    def __init__(self, id: int, nombre: str, descripcion: Optional[str] = None) -> None:
        super().__init__(id)
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: Optional[str]) -> None:
        self._descripcion = valor

    def __repr__(self) -> str:
        return f"TipoCotizacion(id={self._id}, nombre={self._nombre})"

class Libro(EntidadBase):
    """Representa un libro del catálogo de la librería."""

    def __init__(self, id: int, isbn: str, titulo: str, autor: str,
                 genero: Genero, editorial: Editorial, idioma: str,
                 fecha_publicacion: datetime.date, fecha_primera_publicacion: datetime.date,
                 num_paginas: int, peso: float, descripcion: Optional[str] = None,
                 ranking: Optional[int] = None) -> None:
        super().__init__(id)
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._editorial = editorial
        self._idioma = idioma
        self._fecha_publicacion = fecha_publicacion
        self._fecha_primera_publicacion = fecha_primera_publicacion
        self._num_paginas = num_paginas
        self._peso = peso
        self._descripcion = descripcion
        self._ranking = ranking

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        self._isbn = valor

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = valor

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor = valor

    @property
    def genero(self) -> Genero:
        return self._genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        self._genero = valor

    @property
    def editorial(self) -> Editorial:
        return self._editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        self._editorial = valor

    @property
    def idioma(self) -> str:
        return self._idioma

    @idioma.setter
    def idioma(self, valor: str) -> None:
        self._idioma = valor

    @property
    def fecha_publicacion(self) -> datetime.date:
        return self._fecha_publicacion

    @fecha_publicacion.setter
    def fecha_publicacion(self, valor: datetime.date) -> None:
        self._fecha_publicacion = valor

    @property
    def fecha_primera_publicacion(self) -> datetime.date:
        return self._fecha_primera_publicacion

    @fecha_primera_publicacion.setter
    def fecha_primera_publicacion(self, valor: datetime.date) -> None:
        self._fecha_primera_publicacion = valor

    @property
    def num_paginas(self) -> int:
        return self._num_paginas

    @num_paginas.setter
    def num_paginas(self, valor: int) -> None:
        self._num_paginas = valor

    @property
    def peso(self) -> float:
        return self._peso

    @peso.setter
    def peso(self, valor: float) -> None:
        self._peso = valor

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: Optional[str]) -> None:
        self._descripcion = valor

    @property
    def ranking(self) -> Optional[int]:
        return self._ranking

    @ranking.setter
    def ranking(self, valor: Optional[int]) -> None:
        self._ranking = valor

    def __repr__(self) -> str:
        return f"Libro(id={self._id}, isbn={self._isbn}, titulo={self._titulo}, autor={self._autor})"

class Precio(EntidadBase):
    """Representa el precio de un libro en una moneda determinada."""

    def __init__(self, id: int, libro: Libro, moneda: Moneda, valor: float) -> None:
        super().__init__(id)
        self._libro = libro
        self._moneda = moneda
        self._valor = valor

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        self._libro = valor

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        self._moneda = valor

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self._valor = valor

    def __repr__(self) -> str:
        return f"Precio(id={self._id}, libro={self._libro.titulo}, moneda={self._moneda.codigo}, valor={self._valor})"

class Stock(EntidadBase):
    """Representa el stock disponible de un libro en el inventario."""

    def __init__(self, id: int, libro: Libro, cantidad: int,
                 estado: str, ubicacion: str,
                 fecha_ingreso: datetime.date) -> None:
        super().__init__(id)
        self._libro = libro
        self._cantidad = cantidad
        self._estado = estado
        self._ubicacion = ubicacion
        self._fecha_ingreso = fecha_ingreso

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        self._libro = valor

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self._cantidad = valor

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        self._estado = valor

    @property
    def ubicacion(self) -> str:
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor: str) -> None:
        self._ubicacion = valor

    @property
    def fecha_ingreso(self) -> datetime.date:
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, valor: datetime.date) -> None:
        self._fecha_ingreso = valor

    def __repr__(self) -> str:
        return f"Stock(id={self._id}, libro={self._libro.titulo}, cantidad={self._cantidad}, estado={self._estado})"

class CotizacionDolar(EntidadBase):
    """Representa el registro histórico del valor del dólar por tipo y fecha."""

    def __init__(self, id: int, tipo_cotizacion: TipoCotizacion,
                 fecha: datetime.date, valor: float) -> None:
        super().__init__(id)
        self._tipo_cotizacion = tipo_cotizacion
        self._fecha = fecha
        self._valor = valor

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self._tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion) -> None:
        self._tipo_cotizacion = valor

    @property
    def fecha(self) -> datetime.date:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: datetime.date) -> None:
        self._fecha = valor

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self._valor = valor

    def __repr__(self) -> str:
        return f"CotizacionDolar(id={self._id}, tipo={self._tipo_cotizacion.nombre}, fecha={self._fecha}, valor={self._valor})"
