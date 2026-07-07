from abc import ABC, abstractmethod
from typing import Optional

from ...domain.entities.event_webhook import EventoWebhook


class IEventoRepository(ABC):
    @abstractmethod
    async def buscar_por_event_id(self, event_id: str) -> Optional[EventoWebhook]:
        """Verifica se evento já foi processado"""
        pass

    @abstractmethod
    async def criar(self, evento: EventoWebhook) -> EventoWebhook:
        """Registra um novo evento"""
        pass
