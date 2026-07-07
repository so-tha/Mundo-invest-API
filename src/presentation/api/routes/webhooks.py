from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos.webhook_dto import WebhookDTO
from ....application.use_cases.process_webhook_use_case import ProcessarWebhookUseCase
from ....domain.exceptions.domain_exceptions import (
    ClienteNaoEncontradoException,
    EventoDuplicadoException,
)
from ...schemas.webhook_schema import WebhookRequest, WebhookResponse
from ..dependencies import get_processar_webhook_use_case

router = APIRouter()


@router.post(
    "/pipefy/card-updated",
    response_model=WebhookResponse,
    status_code=status.HTTP_200_OK,
    summary="Receber webhook do Pipefy",
    description=(
        "Processa uma notificação de atualização de card enviada pelo Pipefy. "
        "Idempotente: eventos duplicados são aceitos sem reprocessamento."
    ),
)
async def processar_webhook_pipefy(
    request: WebhookRequest,
    use_case: ProcessarWebhookUseCase = Depends(get_processar_webhook_use_case),
):
    try:
        dto = WebhookDTO(**request.model_dump())
        resultado = await use_case.executar(dto)
        return WebhookResponse(**resultado)

    except EventoDuplicadoException as e:
        # Idempotência: retorna 200 sem reprocessar
        return WebhookResponse(
            sucesso=True,
            mensagem=f"Evento já processado anteriormente: {str(e)}",
            duplicado=True,
        )

    except ClienteNaoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar webhook: {str(e)}",
        )
