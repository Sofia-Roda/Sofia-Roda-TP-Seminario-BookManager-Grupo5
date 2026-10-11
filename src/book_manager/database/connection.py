from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker


# Ruta absoluta al archivo de la base en la raíz del proyecto, para que
# funcione sin importar desde qué directorio se ejecute el programa.
RUTA_DB = Path(__file__).resolve().parents[3] / "book_manager.db"


class ConexionDB:
    """Administra la conexión con la base de datos mediante SQLAlchemy."""

    def __init__(self, url: Optional[str] = None, echo: bool = False) -> None:
        """Crea el engine y la fábrica de sesiones.

        Args:
            url (Optional[str]): URL de conexión de SQLAlchemy. Si es None,
                se utiliza un archivo SQLite en la raíz del proyecto.
            echo (bool): Si es True, muestra por consola las sentencias SQL.

        Raises:
            ValueError: Si la URL está vacía.
        """
        if url is None:
            url = f"sqlite:///{RUTA_DB}"
        if not isinstance(url, str) or not url.strip():
            raise ValueError("La URL de conexión no puede estar vacía.")

        self._url = url
        self._engine: Optional[Engine] = create_engine(url, echo=echo)
        if self._engine.dialect.name == "sqlite":
            # SQLite no valida las claves foráneas si no se activa.
            event.listen(self._engine, "connect", _activar_claves_foraneas)

        # Con expire_on_commit=False los objetos siguen siendo legibles
        # después del commit, aunque la sesión ya se haya cerrado.
        self._session_factory = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
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


def _activar_claves_foraneas(conexion_dbapi, _registro) -> None:
    """Activa la validación de claves foráneas en cada conexión SQLite."""
    cursor = conexion_dbapi.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
