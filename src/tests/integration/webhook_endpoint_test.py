import pytest
from httpx import AsyncClient
from datetime import datetime


@pytest.mark.asyncio
async def test_processar_webhook_sucesso(client: AsyncClient):

    cliente_payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000
    }
    await client.post("/clientes/", json=cliente_payload)

    webhook_payload = {
        "event_id": "evt_123",
        "card_id": "card_456",
        "cliente_email": "joao@example.com",
        "timestamp": datetime.now().isoformat()
    }
    
    response = await client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True
    assert data["status"] == "Processado"
    assert data["prioridade"] == "prioridade_alta"


@pytest.mark.asyncio
async def test_processar_webhook_evento_duplicado(client: AsyncClient):
    cliente_payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000
    }
    await client.post("/clientes/", json=cliente_payload)
    
    webhook_payload = {
        "event_id": "evt_123",
        "card_id": "card_456",
        "cliente_email": "joao@example.com",
        "timestamp": datetime.now().isoformat()
    }
    await client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    
    response = await client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True
    assert data["duplicado"] is True


@pytest.mark.asyncio
async def test_processar_webhook_cliente_nao_encontrado(client: AsyncClient):
    """Testa webhook para cliente inexistente"""
    webhook_payload = {
        "event_id": "evt_999",
        "card_id": "card_999",
        "cliente_email": "naoexiste@example.com",
        "timestamp": datetime.now().isoformat()
    }
    
    response = await client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_processar_webhook_prioridade_normal(client: AsyncClient):
    cliente_payload = {
        "cliente_nome": "Maria Santos",
        "cliente_email": "maria@example.com",
        "tipo_solicitacao": "Nova aplicação",
        "valor_patrimonio": 150000  # < 200k
    }
    await client.post("/clientes/", json=cliente_payload)

    webhook_payload = {
        "event_id": "evt_456",
        "card_id": "card_789",
        "cliente_email": "maria@example.com",
        "timestamp": datetime.now().isoformat()
    }
    
    response = await client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True
    assert data["status"] == "Processado"
    assert data["prioridade"] == "prioridade_normal"