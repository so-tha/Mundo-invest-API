from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....application.dtos.create_client_dto import CriarClienteDTO
from ....application.use_cases.create_client_use_case import CriarClienteUseCase
from ....domain.exceptions.domain_exceptions import EmailDuplicadoException
from ....infrastructure.database.connection import get_db_session
from ....infrastructure.database.repositories.client_repository import (
    ClienteRepositoryImpl,
)
from ...schemas.client_schema import (
    ClienteDetailResponse,
    CriarClienteRequest,
    CriarClienteResponse,
    ListarClientesResponse,
)
from ..dependencies import get_criar_cliente_use_case, verify_api_key

router = APIRouter()


@router.post(
    "/",
    response_model=CriarClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    description="Cadastra um novo cliente e enfileira a criação do card no Pipefy.",
    dependencies=[Depends(verify_api_key)],
)
async def criar_cliente(
    request: CriarClienteRequest,
    use_case: CriarClienteUseCase = Depends(get_criar_cliente_use_case),
):
    try:
        dto = CriarClienteDTO(**request.model_dump())
        resultado = await use_case.executar(dto)
        return CriarClienteResponse(**resultado)
    except EmailDuplicadoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar cliente: {str(e)}",
        )


@router.get(
    "/",
    response_model=ListarClientesResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar clientes",
    description="Retorna a lista paginada de clientes cadastrados.",
)
async def listar_clientes(
    limit: int = Query(
        default=20, ge=1, le=100, description="Máximo de itens por página"
    ),
    offset: int = Query(default=0, ge=0, description="Índice inicial (offset)"),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        repository = ClienteRepositoryImpl(session)
        clientes = await repository.listar_todos(limit=limit, offset=offset)

        clientes_response = [
            ClienteDetailResponse(
                id=cliente.id,
                nome=cliente.nome,
                email=cliente.email,
                tipo_solicitacao=cliente.tipo_solicitacao,
                valor_patrimonio=cliente.valor_patrimonio,
                status=cliente.status.value,
                prioridade=cliente.prioridade.value if cliente.prioridade else None,
            )
            for cliente in clientes
        ]

        return ListarClientesResponse(
            sucesso=True,
            total=len(clientes_response),
            limit=limit,
            offset=offset,
            clientes=clientes_response,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar clientes: {str(e)}",
        )
