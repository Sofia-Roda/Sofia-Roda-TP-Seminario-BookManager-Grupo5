"""Contiene la lógica y el decorador para auditar operaciones del sistema."""

import datetime
from functools import wraps
from typing import Any, Callable

from book_manager.entities.entities import Auditoria
from book_manager.repositories.repositories import RepositorioAuditoria


class AuditoriaService:
    """Gestiona el registro y la consulta de auditorías."""

    def __init__(self, repositorio: RepositorioAuditoria) -> None:
        self._repositorio = repositorio

    def registrar(self, accion: str, detalles: str) -> Auditoria:
        """Registra una operación realizada en el sistema."""
        auditorias = self._repositorio.leer_todos()

        nuevo_id = max(
            (auditoria.id for auditoria in auditorias),
            default=0,
        ) + 1

        auditoria = Auditoria(
            id=nuevo_id,
            accion=accion,
            fecha=datetime.datetime.now(),
            detalles=detalles,
        )

        return self._repositorio.crear(auditoria)

    def listar(self) -> list[Auditoria]:
        """Devuelve el historial completo de auditorías."""
        return self._repositorio.leer_todos()


def auditar(accion: str) -> Callable:
    """Crea un decorador que registra una operación del sistema.

    El objeto cuyo método se decora debe disponer del atributo
    `_auditoria_service`.

    Args:
        accion (str): Nombre descriptivo de la acción auditada.

    Returns:
        Callable: Decorador configurado con la acción indicada.
    """

    def decorador(funcion: Callable) -> Callable:

        @wraps(funcion)
        def envoltura(self: Any, *args: Any, **kwargs: Any) -> Any:
            try:
                resultado = funcion(self, *args, **kwargs)

                detalles = (
                    f"{self.__class__.__name__}.{funcion.__name__} "
                    f"ejecutado correctamente. "
                    f"args={args}, kwargs={kwargs}"
                )

                self._auditoria_service.registrar(
                    accion=accion,
                    detalles=detalles,
                )

                return resultado

            except Exception as exc:
                detalles = (
                    f"{self.__class__.__name__}.{funcion.__name__} "
                    f"finalizó con error: "
                    f"{type(exc).__name__}: {exc}. "
                    f"args={args}, kwargs={kwargs}"
                )

                self._auditoria_service.registrar(
                    accion=accion,
                    detalles=detalles,
                )

                raise

        return envoltura

    return decorador