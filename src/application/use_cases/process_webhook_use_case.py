from typing import Dict, Any
from datetime import datetime
from ..dtos.webhook_dto import WebhookDTO
from ..interfaces.client_repository import IClienteRepository
from ..interfaces.event_repository import IEventoRepository
from ..interfaces.pipefy_gateway import IPipefyGateway
from ...domain.entities.event_webhook import EventoWebhook
from ...domain.exceptions.domain_exceptions import (
    EventoDuplicadoException,
    ClienteNaoEncontradoException
)


class ProcessarWebhookUseCase:
    def __init__(
        self,
        cliente_repository: IClienteRepository,
        evento_repository: IEventoRepository,
        pipefy_gateway: IPipefyGateway
    ):
        self._cliente_repository = cliente_repository
        self._evento_repository = evento_repository
        self._pipefy_gateway = pipefy_gateway
    
    async def executar(self, dto: WebhookDTO) -> Dict[str, Any]:
        evento_existente = await self._evento_repository.buscar_por_event_id(
            dto.event_id
        )
        
        if evento_existente:
            raise EventoDuplicadoException(
                f"Evento {dto.event_id} já foi processado"
            )
        
        cliente = await self._cliente_repository.buscar_por_email(
            dto.cliente_email
        )
        
        if not cliente:
            raise ClienteNaoEncontradoException(
                f"Cliente com email {dto.cliente_email} não encontrado"
            )
        
        cliente.processar()  
        pipefy_mutation = await self._pipefy_gateway.atualizar_card(
            card_id=dto.card_id,
            status=cliente.status.value,
            prioridade=cliente.prioridade.value
        )
        
        await self._cliente_repository.atualizar(cliente)

        evento = EventoWebhook(
            event_id=dto.event_id,
            card_id=dto.card_id,
            cliente_email=dto.cliente_email,
            timestamp=dto.timestamp
        )
        evento.marcar_como_processado()
        await self._evento_repository.criar(evento)
        
        return {
            "sucesso": True,
            "mensagem": "Webhook processado com sucesso",
            "cliente_email": cliente.email,
            "status": cliente.status.value,
            "prioridade": cliente.prioridade.value,
            "pipefy_mutation": pipefy_mutation
        }