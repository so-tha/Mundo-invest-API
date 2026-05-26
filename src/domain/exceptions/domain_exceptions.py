class DomainException(Exception):
    """Exceção base do domínio"""
    pass


class EventoDuplicadoException(DomainException):
    """Evento já foi processado anteriormente"""
    pass


class ClienteNaoEncontradoException(DomainException):
    """Cliente não encontrado no banco"""
    pass