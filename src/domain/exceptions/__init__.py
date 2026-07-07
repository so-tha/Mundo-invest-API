from .domain_exceptions import ClienteNaoEncontradoException  # noqa: F401
from .domain_exceptions import (
    DomainException,
    EmailDuplicadoException,
    EventoDuplicadoException,
)

__all__ = [
    "DomainException",
    "EmailDuplicadoException",
    "EventoDuplicadoException",
    "ClienteNaoEncontradoException",
]
