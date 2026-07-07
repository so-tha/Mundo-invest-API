from datetime import datetime

from src.domain.entities.event_webhook import EventoWebhook


def test_criar_evento_webhook():
    """Testa criação de evento webhook"""
    evento = EventoWebhook(
        event_id="evt_123",
        card_id="card_456",
        cliente_email="joao@example.com",
        timestamp=datetime.now(),
    )

    assert evento.event_id == "evt_123"
    assert evento.processado is False


def test_marcar_evento_como_processado():
    """Testa marcação de evento como processado"""
    evento = EventoWebhook(
        event_id="evt_123",
        card_id="card_456",
        cliente_email="joao@example.com",
        timestamp=datetime.now(),
    )

    evento.marcar_como_processado()

    assert evento.processado is True
    assert evento.processado_em is not None
