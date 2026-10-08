
import datetime
from typing import Optional


# Validaciones reutilizadas por los setters de las entidades

def _validar_texto(valor: str, campo: str) -> str:
    """Verifica que el valor sea un texto no vacío."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo {campo} no puede estar vacío.")
    return valor


def _validar_texto_opcional(valor: Optional[str], campo: str) -> Optional[str]:
    """Verifica que el valor sea None o un texto."""
    if valor is not None and not isinstance(valor, str):
        raise TypeError(f"El campo {campo} debe ser un texto.")
    return valor


def _validar_entero(valor: int, campo: str, minimo: int) -> int:
    """Verifica que el valor sea un entero mayor o igual al mínimo."""
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError(f"El campo {campo} debe ser un número entero.")
    if valor < minimo:
        raise ValueError(f"El campo {campo} debe ser mayor o igual a {minimo}.")
    return valor


def _validar_positivo(valor: float, campo: str) -> float:
    """Verifica que el valor sea un número mayor a cero."""
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        raise TypeError(f"El campo {campo} debe ser numérico.")
    if valor <= 0:
        raise ValueError(f"El campo {campo} debe ser mayor a cero.")
    return float(valor)


def _validar_fecha(valor: datetime.date, campo: str) -> datetime.date:
    """Verifica que el valor sea una fecha."""
    if not isinstance(valor, datetime.date):
        raise TypeError(f"El campo {campo} debe ser una fecha.")
    return valor


def _validar_instancia(valor: object, clase: type, campo: str) -> object:
    """Verifica que el valor sea una instancia de la clase indicada."""
    if not isinstance(valor, clase):
        raise TypeError(f"El campo {campo} debe ser de tipo {clase.__name__}.")
    return valor


class EntidadBase:
    """Clase base para todas las entidades del sistema."""

    def __init__(self, id: int) -> None:
        # El id es de solo lectura: identifica a la entidad y no debe cambiar.
        self._id = _validar_entero(id, "id", 1)

    @property
    def id(self) -> int:
        return self._id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"


class Genero(EntidadBase):
    """Representa una categoría literaria de un libro."""

    def __init__(self, id: int, nombre: str, descripcion: Optional[str] = None) -> None:
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: Optional[str]) -> None:
        self._descripcion = _validar_texto_opcional(valor, "descripción")

    def __repr__(self) -> str:
        return f"Genero(id={self._id}, nombre={self._nombre})"


class Editorial(EntidadBase):
    """Representa una editorial proveedora de libros."""

    def __init__(self, id: int, nombre: str, cuit: str, email: str,
                 telefono: str, pais: str) -> None:
        super().__init__(id)
        self.nombre = nombre
        self.cuit = cuit
        self.email = email
        self.telefono = telefono
        self.pais = pais

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def cuit(self) -> str:
        return self._cuit

    @cuit.setter
    def cuit(self, valor: str) -> None:
        _validar_texto(valor, "CUIT")
        solo_digitos = valor.replace("-", "")
        if not solo_digitos.isdigit() or len(solo_digitos) != 11:
            raise ValueError(f"CUIT inválido: {valor}. Debe tener 11 dígitos.")
        self._cuit = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        _validar_texto(valor, "email")
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError(f"Email inválido: {valor}.")
        self._email = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = _validar_texto(valor, "teléfono")

    @property
    def pais(self) -> str:
        return self._pais

    @pais.setter
    def pais(self, valor: str) -> None:
        self._pais = _validar_texto(valor, "país")

    def __repr__(self) -> str:
        return f"Editorial(id={self._id}, nombre={self._nombre}, pais={self._pais})"

class Moneda(EntidadBase):
    """Representa un tipo de moneda utilizada en el sistema."""

    def __init__(self, id: int, nombre: str, simbolo: str, codigo: str) -> None:
        super().__init__(id)
        self.nombre = nombre
        self.simbolo = simbolo
        self.codigo = codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        self._simbolo = _validar_texto(valor, "símbolo")

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        _validar_texto(valor, "código")
        if not valor.isalpha() or len(valor) != 3:
            raise ValueError(f"Código de moneda inválido: {valor}. Deben ser 3 letras (ej. USD).")
        self._codigo = valor.upper()

    def __repr__(self) -> str:
        return f"Moneda(id={self._id}, nombre={self._nombre}, codigo={self._codigo})"

class TipoCotizacion(EntidadBase):
    """Representa un tipo de cotización del dólar (Oficial, Blue, MEP, etc.)."""

    def __init__(self, id: int, nombre: str, descripcion: Optional[str] = None) -> None:
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: Optional[str]) -> None:
        self._descripcion = _validar_texto_opcional(valor, "descripción")

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
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.editorial = editorial
        self.idioma = idioma
        self.establecer_fechas(fecha_publicacion, fecha_primera_publicacion)
        self.num_paginas = num_paginas
        self.peso = peso
        self.descripcion = descripcion
        self.ranking = ranking

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        _validar_texto(valor, "ISBN")
        solo_digitos = valor.replace("-", "")
        if not solo_digitos.isdigit() or len(solo_digitos) not in (10, 13):
            raise ValueError(f"ISBN inválido: {valor}. Debe tener 10 o 13 dígitos.")
        self._isbn = valor

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = _validar_texto(valor, "título")

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor = _validar_texto(valor, "autor")

    @property
    def genero(self) -> Genero:
        return self._genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        self._genero = _validar_instancia(valor, Genero, "género")

    @property
    def editorial(self) -> Editorial:
        return self._editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        self._editorial = _validar_instancia(valor, Editorial, "editorial")

    @property
    def idioma(self) -> str:
        return self._idioma

    @idioma.setter
    def idioma(self, valor: str) -> None:
        self._idioma = _validar_texto(valor, "idioma")

    @property
    def fecha_publicacion(self) -> datetime.date:
        return self._fecha_publicacion

    @fecha_publicacion.setter
    def fecha_publicacion(self, valor: datetime.date) -> None:
        self.establecer_fechas(valor, self._fecha_primera_publicacion)

    @property
    def fecha_primera_publicacion(self) -> datetime.date:
        return self._fecha_primera_publicacion

    @fecha_primera_publicacion.setter
    def fecha_primera_publicacion(self, valor: datetime.date) -> None:
        self.establecer_fechas(self._fecha_publicacion, valor)

    def establecer_fechas(self, fecha_publicacion: datetime.date,
                          fecha_primera_publicacion: datetime.date) -> None:
        """Asigna ambas fechas juntas, validando que sean coherentes.

        Permite cambiar las dos a la vez sin que falle la validación por el
        orden en que se asignan.
        """
        _validar_fecha(fecha_publicacion, "fecha de publicación")
        _validar_fecha(fecha_primera_publicacion, "fecha de primera publicación")
        if fecha_primera_publicacion > fecha_publicacion:
            raise ValueError(
                "La fecha de primera publicación no puede ser posterior "
                "a la fecha de publicación."
            )
        self._fecha_publicacion = fecha_publicacion
        self._fecha_primera_publicacion = fecha_primera_publicacion

    @property
    def num_paginas(self) -> int:
        return self._num_paginas

    @num_paginas.setter
    def num_paginas(self, valor: int) -> None:
        self._num_paginas = _validar_entero(valor, "número de páginas", 1)

    @property
    def peso(self) -> float:
        return self._peso

    @peso.setter
    def peso(self, valor: float) -> None:
        self._peso = _validar_positivo(valor, "peso")

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: Optional[str]) -> None:
        self._descripcion = _validar_texto_opcional(valor, "descripción")

    @property
    def ranking(self) -> Optional[int]:
        return self._ranking

    @ranking.setter
    def ranking(self, valor: Optional[int]) -> None:
        self._ranking = None if valor is None else _validar_entero(valor, "ranking", 1)

    def __repr__(self) -> str:
        return f"Libro(id={self._id}, isbn={self._isbn}, titulo={self._titulo}, autor={self._autor})"

class Precio(EntidadBase):
    """Representa el precio de un libro en una moneda determinada."""

    def __init__(self, id: int, libro: Libro, moneda: Moneda, valor: float) -> None:
        super().__init__(id)
        self.libro = libro
        self.moneda = moneda
        self.valor = valor

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        self._libro = _validar_instancia(valor, Libro, "libro")

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        self._moneda = _validar_instancia(valor, Moneda, "moneda")

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self._valor = _validar_positivo(valor, "valor")

    def __repr__(self) -> str:
        return f"Precio(id={self._id}, libro={self._libro.titulo}, moneda={self._moneda.codigo}, valor={self._valor})"

class Stock(EntidadBase):
    """Representa el stock disponible de un libro en el inventario."""

    def __init__(self, id: int, libro: Libro, cantidad: int,
                 estado: str, ubicacion: str,
                 fecha_ingreso: datetime.date) -> None:
        super().__init__(id)
        self.libro = libro
        self.cantidad = cantidad
        self.estado = estado
        self.ubicacion = ubicacion
        self.fecha_ingreso = fecha_ingreso

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        self._libro = _validar_instancia(valor, Libro, "libro")

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self._cantidad = _validar_entero(valor, "cantidad", 0)

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        self._estado = _validar_texto(valor, "estado")

    @property
    def ubicacion(self) -> str:
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor: str) -> None:
        self._ubicacion = _validar_texto(valor, "ubicación")

    @property
    def fecha_ingreso(self) -> datetime.date:
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, valor: datetime.date) -> None:
        self._fecha_ingreso = _validar_fecha(valor, "fecha de ingreso")

    def __repr__(self) -> str:
        return f"Stock(id={self._id}, libro={self._libro.titulo}, cantidad={self._cantidad}, estado={self._estado})"

class CotizacionDolar(EntidadBase):
    """Representa el registro histórico del valor del dólar por tipo y fecha."""

    def __init__(self, id: int, tipo_cotizacion: TipoCotizacion,
                 fecha: datetime.date, valor: float) -> None:
        super().__init__(id)
        self.tipo_cotizacion = tipo_cotizacion
        self.fecha = fecha
        self.valor = valor

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self._tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion) -> None:
        self._tipo_cotizacion = _validar_instancia(valor, TipoCotizacion, "tipo de cotización")

    @property
    def fecha(self) -> datetime.date:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: datetime.date) -> None:
        self._fecha = _validar_fecha(valor, "fecha")

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self._valor = _validar_positivo(valor, "valor")

    def __repr__(self) -> str:
        return f"CotizacionDolar(id={self._id}, tipo={self._tipo_cotizacion.nombre}, fecha={self._fecha}, valor={self._valor})"
