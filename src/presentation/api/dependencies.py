from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...infrastructure.database.connection import get_db_session
from ...infrastructure.database.repositories.client_repository import ClienteRepositoryImpl
from ...infrastructure.database.repositories.event_repository import EventoRepositoryImpl
from ...infrastructure.external.pipefy_gateway_impl import PipefyGatewayImpl
from ...application.use_cases.create_client_use_case import CriarClienteUseCase
from ...application.use_cases.process_webhook_use_case import ProcessarWebhookUseCase


async def get_criar_cliente_use_case(
    session: AsyncSession = Depends(get_db_session)
) -> CriarClienteUseCase:
    cliente_repository = ClienteRepositoryImpl(session)
    pipefy_gateway = PipefyGatewayImpl()
    
    return CriarClienteUseCase(
        cliente_repository=cliente_repository,
        pipefy_gateway=pipefy_gateway
    )


async def get_processar_webhook_use_case(
    session: AsyncSession = Depends(get_db_session)
) -> ProcessarWebhookUseCase:
    cliente_repository = ClienteRepositoryImpl(session)
    evento_repository = EventoRepositoryImpl(session)
    pipefy_gateway = PipefyGatewayImpl()
    
    return ProcessarWebhookUseCase(
        cliente_repository=cliente_repository,
        evento_repository=evento_repository,
        pipefy_gateway=pipefy_gateway
    )