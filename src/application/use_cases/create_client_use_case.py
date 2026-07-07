import logging
from typing import Any, Dict

from ...domain.entities.client import Cliente
from ...domain.enums.status_client import StatusCliente
from ...domain.exceptions.domain_exceptions import EmailDuplicadoException
from ..dtos.create_client_dto import CriarClienteDTO
from ..interfaces.client_repository import IClienteRepository
from ..interfaces.pipefy_gateway import IPipefyGateway

logger = logging.getLogger(__name__)


class CriarClienteUseCase:
    def __init__(
        self, cliente_repository: IClienteRepository, pipefy_gateway: IPipefyGateway
    ):
        self._cliente_repository = cliente_repository
        self._pipefy_gateway = pipefy_gateway

    async def executar(self, dto: CriarClienteDTO) -> Dict[str, Any]:

        logger.info(f"Iniciando criação de cliente: {dto.cliente_email}")

        cliente_existente = await self._cliente_repository.buscar_por_email(
            dto.cliente_email
        )
        if cliente_existente:
            logger.warning(f"Email duplicado: {dto.cliente_email}")
            raise EmailDuplicadoException(
                f"Email '{dto.cliente_email}' já está cadastrado no sistema"
            )

        cliente = Cliente(
            nome=dto.cliente_nome,
            email=dto.cliente_email,
            tipo_solicitacao=dto.tipo_solicitacao,
            valor_patrimonio=dto.valor_patrimonio,
            status=StatusCliente.AGUARDANDO_ANALISE,
        )
        logger.info(f"✓ Entidade criada: {cliente.email}")

        cliente_salvo = await self._cliente_repository.criar(cliente)
        logger.info(f"✓ Cliente salvo com ID: {cliente_salvo.id}")

        pipefy_mutation = await self._pipefy_gateway.criar_card(
            nome=cliente_salvo.nome,
            email=cliente_salvo.email,
            tipo_solicitacao=cliente_salvo.tipo_solicitacao,
            valor_patrimonio=cliente_salvo.valor_patrimonio,
        )
        logger.info("📋 Mutation Pipefy gerada")

        return {
            "sucesso": True,
            "mensagem": "Cliente cadastrado com sucesso",
            "cliente_id": cliente_salvo.id,
            "status": cliente_salvo.status.value,
            "pipefy_card_enqueued": pipefy_mutation.get("sucesso", False),
        }
