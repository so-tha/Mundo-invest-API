import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_criar_cliente_sucesso(client: AsyncClient):
    """Testa criação de cliente via API"""
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000,
    }

    response = await client.post("/clientes/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["sucesso"] is True
    assert data["status"] == "Aguardando Análise"
    assert "cliente_id" in data


@pytest.mark.asyncio
async def test_criar_cliente_email_invalido(client: AsyncClient):
    """Testa criação com email inválido"""
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "email_invalido",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000,
    }

    response = await client.post("/clientes/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_criar_cliente_patrimonio_negativo(client: AsyncClient):
    """Testa criação com patrimônio negativo"""
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": -1000,
    }

    response = await client.post("/clientes/", json=payload)

    assert response.status_code == 422
