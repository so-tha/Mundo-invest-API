"""Implementações de repositórios"""

from .client_repository import ClienteRepositoryImpl  # noqa: F401
from .event_repository import EventoRepositoryImpl  # noqa: F401

__all__ = [
    "ClienteRepositoryImpl",
    "EventoRepositoryImpl",
]
