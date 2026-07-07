from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class EventoWebhook:

    event_id: str
    card_id: str
    cliente_email: str
    timestamp: datetime
    processado: bool = False
    id: Optional[int] = None
    processado_em: Optional[datetime] = None

    def marcar_como_processado(self):
        self.processado = True
        self.processado_em = datetime.now(timezone.utc)
