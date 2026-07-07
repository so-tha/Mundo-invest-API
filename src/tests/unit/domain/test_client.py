import pytest

from src.domain.entities.client import Cliente
from src.domain.enums.priority import Prioridade
from src.domain.enums.status_client import StatusCliente


def test_criar_cliente_valido():
    """Testa criação de cliente com dados válidos"""
    cliente = Cliente(
        nome="João Silva",
        email="joao@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000,
        status=StatusCliente.AGUARDANDO_ANALISE,
    )

    assert cliente.nome == "João Silva"
    assert cliente.email == "joao@example.com"
    assert cliente.valor_patrimonio == 250000


def test_cliente_sem_nome_deve_falhar():
    """Testa que cliente sem nome lança exceção"""
    with pytest.raises(ValueError, match="Nome do cliente é obrigatório"):
        Cliente(
            nome="",
            email="joao@example.com",
            tipo_solicitacao="Atualização cadastral",
            valor_patrimonio=250000,
            status=StatusCliente.AGUARDANDO_ANALISE,
        )


def test_cliente_email_invalido_deve_falhar():
    """Testa que email inválido lança exceção"""
    with pytest.raises(ValueError, match="Email inválido"):
        Cliente(
            nome="João Silva",
            email="email_invalido",
            tipo_solicitacao="Atualização cadastral",
            valor_patrimonio=250000,
            status=StatusCliente.AGUARDANDO_ANALISE,
        )


def test_cliente_patrimonio_negativo_deve_falhar():
    """Testa que patrimônio negativo lança exceção"""
    with pytest.raises(ValueError, match="Patrimônio não pode ser negativo"):
        Cliente(
            nome="João Silva",
            email="joao@example.com",
            tipo_solicitacao="Atualização cadastral",
            valor_patrimonio=-1000,
            status=StatusCliente.AGUARDANDO_ANALISE,
        )


def test_calcular_prioridade_alta():
    """Testa cálculo de prioridade alta (≥ 200k)"""
    cliente = Cliente(
        nome="João Silva",
        email="joao@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000,
        status=StatusCliente.AGUARDANDO_ANALISE,
    )

    prioridade = cliente.calcular_prioridade()
    assert prioridade == Prioridade.ALTA


def test_calcular_prioridade_normal():
    """Testa cálculo de prioridade normal (< 200k)"""
    cliente = Cliente(
        nome="Maria Santos",
        email="maria@example.com",
        tipo_solicitacao="Nova aplicação",
        valor_patrimonio=150000,
        status=StatusCliente.AGUARDANDO_ANALISE,
    )

    prioridade = cliente.calcular_prioridade()
    assert prioridade == Prioridade.NORMAL


def test_processar_cliente():
    """Testa processamento do cliente"""
    cliente = Cliente(
        nome="João Silva",
        email="joao@example.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=250000,
        status=StatusCliente.AGUARDANDO_ANALISE,
    )

    cliente.processar()

    assert cliente.status == StatusCliente.PROCESSADO
    assert cliente.prioridade == Prioridade.ALTA
    assert cliente.atualizado_em is not None
