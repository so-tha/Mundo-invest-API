from abc import ABC, abstractmethod
from typing import Optional
from ...domain.entities.client import Cliente


class IClienteRepository(ABC):
    @abstractmethod
    async def criar(self, cliente: Cliente) -> Cliente:
        """Cria um novo cliente"""
        pass

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        pass

    @abstractmethod
    async def atualizar(self, cliente: Cliente) -> Cliente:
        """Atualiza dados do cliente"""
        pass

    @abstractmethod
    async def listar_todos(self, limit: int = 20, offset: int = 0) -> list:
        """Lista clientes com paginação"""
        pass