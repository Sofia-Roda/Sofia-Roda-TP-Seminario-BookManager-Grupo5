from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class GeneroModel(Base):
    """Modelo de base de datos para los géneros."""

    __tablename__ = "generos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    libros = relationship("LibroModel", back_populates="genero")


class EditorialModel(Base):
    """Modelo de base de datos para las editoriales."""

    __tablename__ = "editoriales"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    cuit = Column(String(20), nullable=False)
    email = Column(String(150), nullable=False)
    telefono = Column(String(50), nullable=False)
    pais = Column(String(100), nullable=False)

    libros = relationship("LibroModel", back_populates="editorial")


class MonedaModel(Base):
    """Modelo de base de datos para las monedas."""

    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    simbolo = Column(String(10), nullable=False)
    codigo = Column(String(10),nullable=False,unique=True,)

    precios = relationship("PrecioModel", back_populates="moneda")


class TipoCotizacionModel(Base):
    """Modelo de base de datos para los tipos de cotización."""

    __tablename__ = "tipos_cotizacion"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    cotizaciones = relationship("CotizacionDolarModel", back_populates="tipo_cotizacion")


class LibroModel(Base):
    """Modelo de base de datos para los libros."""

    __tablename__ = "libros"

    id = Column(Integer, primary_key=True)
    isbn = Column(String(30),nullable=False,unique=True,)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)

    genero_id = Column(Integer, ForeignKey("generos.id"), nullable=False)
    editorial_id = Column(Integer, ForeignKey("editoriales.id"), nullable=False)

    idioma = Column(String(50), nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    fecha_primera_publicacion = Column(Date, nullable=False)
    num_paginas = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)
    ranking = Column(Integer, nullable=True)

    genero = relationship("GeneroModel", back_populates="libros")
    editorial = relationship("EditorialModel", back_populates="libros")
    precios = relationship("PrecioModel", back_populates="libro")
    stock = relationship("StockModel", back_populates="libro", uselist=False)


class PrecioModel(Base):
    """Modelo de base de datos para los precios."""

    __tablename__ = "precios"

    id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    moneda_id = Column(Integer, ForeignKey("monedas.id"), nullable=False)
    valor = Column(Float, nullable=False)

    libro = relationship("LibroModel", back_populates="precios")
    moneda = relationship("MonedaModel", back_populates="precios")


class StockModel(Base):
    """Modelo de base de datos para el stock."""

    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False, unique=True)
    cantidad = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False)
    ubicacion = Column(String(100), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)

    libro = relationship("LibroModel", back_populates="stock")


class CotizacionDolarModel(Base):
    """Modelo de base de datos para las cotizaciones del dólar."""

    __tablename__ = "cotizaciones_dolar"

    id = Column(Integer, primary_key=True)
    tipo_cotizacion_id = Column(Integer, ForeignKey("tipos_cotizacion.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    compra = Column(Float, nullable=True)
    valor = Column(Float, nullable=False)

    tipo_cotizacion = relationship("TipoCotizacionModel", back_populates="cotizaciones")

    __table_args__ = (
        UniqueConstraint("tipo_cotizacion_id", "fecha", name="uq_tipo_cotizacion_fecha"),
    )