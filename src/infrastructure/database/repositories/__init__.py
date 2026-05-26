"""Implementações de repositórios"""
from .client_repository import ClienteRepositoryImpl
from .event_repository import EventoRepositoryImpl

__all__ = [
    "ClienteRepositoryImpl",
    "EventoRepositoryImpl",
]