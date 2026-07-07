"""Entidades de domínio"""

from .client import Cliente  # noqa: F401
from .event_webhook import EventoWebhook  # noqa: F401

__all__ = [
    "Cliente",
    "EventoWebhook",
]
