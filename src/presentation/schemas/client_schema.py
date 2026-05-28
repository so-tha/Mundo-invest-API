from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CriarClienteRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cliente_nome": "João Silva",
                "cliente_email": "joao.silva@example.com",
                "tipo_solicitacao": "Atualização cadastral",
                "valor_patrimonio": 250000,
            }
        }
    )

    cliente_nome: str = Field(..., min_length=1, description="Nome completo do cliente")
    cliente_email: EmailStr = Field(..., description="Email válido do cliente")
    tipo_solicitacao: str = Field(..., min_length=1, description="Tipo da solicitação")
    valor_patrimonio: float = Field(..., ge=0, description="Patrimônio em reais")


class CriarClienteResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sucesso": True,
                "mensagem": "Cliente cadastrado com sucesso",
                "cliente_id": 123,
                "status": "Aguardando Análise",
                "pipefy_mutation": {
                    "mutation": "...",
                    "variables": {},
                },
            }
        }
    )

    sucesso: bool
    mensagem: str
    cliente_id: int
    status: str
    pipefy_mutation: Optional[dict] = None


class ClienteDetailResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 123,
                "nome": "João Silva",
                "email": "joao.silva@example.com",
                "tipo_solicitacao": "Atualização cadastral",
                "valor_patrimonio": 250000,
                "status": "Aguardando Análise",
                "prioridade": None,
            }
        }
    )

    id: int
    nome: str
    email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: Optional[str] = None


class ListarClientesResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sucesso": True,
                "total": 2,
                "clientes": [
                    {
                        "id": 1,
                        "nome": "João Silva",
                        "email": "joao@example.com",
                        "tipo_solicitacao": "Atualização cadastral",
                        "valor_patrimonio": 250000,
                        "status": "Aguardando Análise",
                        "prioridade": None,
                    }
                ],
            }
        }
    )

    sucesso: bool
    total: int
    clientes: list[ClienteDetailResponse]
