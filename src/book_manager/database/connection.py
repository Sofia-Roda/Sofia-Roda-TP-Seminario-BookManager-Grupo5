import os
from contextlib import contextmanager
from typing import Iterator, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()


class ConexionDB:
    """Administra la conexión con la base de datos mediante SQLAlchemy."""

    def __init__(
        self,
        url: Optional[str] = None,
        echo: bool = False,
    ) -> None:
        """Crea el engine y la fábrica de sesiones.

        Args:
            url (Optional[str]): URL de conexión de SQLAlchemy. Si es None,
                se busca la variable DATABASE_URL en el archivo .env.
            echo (bool): Si es True, muestra por consola las sentencias SQL.

        Raises:
            ValueError: Si DATABASE_URL no está configurada.
            ConnectionError: Si no se puede establecer la conexión.
        """
        if url is None:
            url = os.getenv("DATABASE_URL")

        if not isinstance(url, str) or not url.strip():
            raise ValueError(
                "No se encontró DATABASE_URL para conectar con la base de datos."
            )

        self._url = url
        self._engine: Optional[Engine] = create_engine(
            url,
            echo=echo,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

        if not self.probar_conexion():
            self.cerrar()
            raise ConnectionError(
                "No se pudo establecer la conexión con la base de datos."
            )

    @property
    def url(self) -> str:
        return self._url

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            raise RuntimeError("La conexión a la base de datos está cerrada.")
        return self._engine

    def crear_sesion(self) -> Session:
        """Crea una nueva sesión con la base de datos.

        Returns:
            Session: Sesión de SQLAlchemy asociada al engine.

        Raises:
            RuntimeError: Si la conexión fue cerrada.
        """
        if self._engine is None:
            raise RuntimeError("La conexión a la base de datos está cerrada.")
        return self._session_factory()

    @contextmanager
    def transaccion(self) -> Iterator[Session]:
        """Context manager que maneja una transacción con la base de datos.

        Confirma los cambios (commit) si el bloque termina sin errores,
        los deshace (rollback) si ocurre una excepción y siempre cierra
        la sesión al finalizar.

        Yields:
            Session: Sesión de SQLAlchemy para operar dentro del bloque.

        Raises:
            Exception: Relanza la excepción ocurrida dentro del bloque,
                luego de deshacer los cambios.
        """
        sesion = self.crear_sesion()
        try:
            yield sesion
            sesion.commit()
        except Exception:
            sesion.rollback()
            raise
        finally:
            sesion.close()

    def probar_conexion(self) -> bool:
        """Verifica que la base de datos responda.

        Returns:
            bool: True si la conexión es exitosa, False en caso contrario.
        """
        try:
            with self.engine.connect() as conexion:
                conexion.execute(text("SELECT 1"))
            return True
        except (SQLAlchemyError, RuntimeError):
            return False

    def cerrar(self) -> None:
        """Libera las conexiones abiertas del engine."""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

