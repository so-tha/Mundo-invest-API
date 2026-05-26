from abc import ABC, abstractmethod
from typing import Dict, Any


class IPipefyGateway(ABC):
    @abstractmethod
    async def criar_card(
        self,
        nome: str,
        email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float
    ) -> Dict[str, Any]:
        """Estrutura a mutation createCard do Pipefy"""
        pass
    
    @abstractmethod
    async def atualizar_card(
        self,
        card_id: str,
        status: str,
        prioridade: str
    ) -> Dict[str, Any]:
        """Estrutura a mutation updateCardField do Pipefy"""
        pass