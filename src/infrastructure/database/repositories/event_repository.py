from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....application.interfaces.event_repository import IEventoRepository
from ....domain.entities.event_webhook import EventoWebhook
from ..models import EventoWebhookModel


class EventoRepositoryImpl(IEventoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def buscar_por_event_id(self, event_id: str) -> Optional[EventoWebhook]:
        result = await self._session.execute(
            select(EventoWebhookModel).where(EventoWebhookModel.event_id == event_id)
        )
        db_evento = result.scalar_one_or_none()

        if not db_evento:
            return None

        return self._to_entity(db_evento)

    async def criar(self, evento: EventoWebhook) -> EventoWebhook:
        db_evento = EventoWebhookModel(
            event_id=evento.event_id,
            card_id=evento.card_id,
            cliente_email=evento.cliente_email,
            timestamp=evento.timestamp,
            processado=evento.processado,
            processado_em=evento.processado_em,
        )

        self._session.add(db_evento)
        await self._session.commit()
        await self._session.refresh(db_evento)

        return self._to_entity(db_evento)

    @staticmethod
    def _to_entity(model: EventoWebhookModel) -> EventoWebhook:
        return EventoWebhook(
            id=model.id,
            event_id=model.event_id,
            card_id=model.card_id,
            cliente_email=model.cliente_email,
            timestamp=model.timestamp,
            processado=model.processado,
            processado_em=model.processado_em,
        )
