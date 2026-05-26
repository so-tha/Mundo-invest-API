"""Entidades de domínio"""
from .client import Cliente
from .event_webhook import EventoWebhook

__all__ = [
    "Cliente",
    "EventoWebhook",
]