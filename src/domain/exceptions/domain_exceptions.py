class DomainException(Exception):
    """Exceção base do domínio"""

    pass


class EmailDuplicadoException(DomainException):
    """Email já cadastrado no sistema"""

    pass


class EventoDuplicadoException(DomainException):
    """Evento já foi processado anteriormente"""

    pass


class ClienteNaoEncontradoException(DomainException):
    """Cliente não encontrado no banco"""

    pass
