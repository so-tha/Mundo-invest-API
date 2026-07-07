from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.use_cases.create_client_use_case import CriarClienteUseCase
from ...application.use_cases.process_webhook_use_case import ProcessarWebhookUseCase
from ...infrastructure.config.settings import settings
from ...infrastructure.database.connection import get_db_session
from ...infrastructure.database.repositories.client_repository import (
    ClienteRepositoryImpl,
)
from ...infrastructure.database.repositories.event_repository import (
    EventoRepositoryImpl,
)
from ...infrastructure.external.pipefy_gateway_impl import PipefyGatewayImpl

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(_api_key_header)) -> None:
    """
    Valida a API Key enviada no header X-API-Key.

    """
    if settings.api_key is None:
        return

    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida ou ausente. Envie o header X-API-Key.",
        )


def _get_pipefy_gateway() -> PipefyGatewayImpl:
    """Instancia o gateway Pipefy — modo real ou stub conforme configuração."""
    return PipefyGatewayImpl(
        api_token=settings.pipefy_api_token,
        pipe_id=settings.pipefy_pipe_id,
    )


async def get_criar_cliente_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> CriarClienteUseCase:
    cliente_repository = ClienteRepositoryImpl(session)
    pipefy_gateway = _get_pipefy_gateway()

    return CriarClienteUseCase(
        cliente_repository=cliente_repository,
        pipefy_gateway=pipefy_gateway,
    )


async def get_processar_webhook_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> ProcessarWebhookUseCase:
    cliente_repository = ClienteRepositoryImpl(session)
    evento_repository = EventoRepositoryImpl(session)
    pipefy_gateway = _get_pipefy_gateway()

    return ProcessarWebhookUseCase(
        cliente_repository=cliente_repository,
        evento_repository=evento_repository,
        pipefy_gateway=pipefy_gateway,
    )
