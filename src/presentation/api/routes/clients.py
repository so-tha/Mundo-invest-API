from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.client_schema import CriarClienteRequest, CriarClienteResponse, ListarClientesResponse, ClienteDetailResponse
from ....application.use_cases.create_client_use_case import CriarClienteUseCase
from ....application.dtos.create_client_dto import CriarClienteDTO
from ....infrastructure.database.repositories.client_repository import ClienteRepositoryImpl
from ....infrastructure.database.connection import get_db_session
from ..dependencies import get_criar_cliente_use_case

router = APIRouter()


@router.post(
    "/",
    response_model=CriarClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente"
)
async def criar_cliente(
    request: CriarClienteRequest,
    use_case: CriarClienteUseCase = Depends(get_criar_cliente_use_case)
):
    try:
        dto = CriarClienteDTO(**request.model_dump())
        resultado = await use_case.executar(dto)
        return CriarClienteResponse(**resultado)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


@router.get(
    "/",
    response_model=ListarClientesResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar todos os clientes"
)
async def listar_clientes(session: AsyncSession = Depends(get_db_session)):
    try:
        repository = ClienteRepositoryImpl(session)
        clientes = await repository.listar_todos()
        
        clientes_response = [
            ClienteDetailResponse(
                id=cliente.id,
                nome=cliente.nome,
                email=cliente.email,
                tipo_solicitacao=cliente.tipo_solicitacao,
                valor_patrimonio=cliente.valor_patrimonio,
                status=cliente.status.value,
                prioridade=cliente.prioridade.value if cliente.prioridade else None
            )
            for cliente in clientes
        ]
        
        return ListarClientesResponse(
            sucesso=True,
            total=len(clientes_response),
            clientes=clientes_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar clientes: {str(e)}"
        )