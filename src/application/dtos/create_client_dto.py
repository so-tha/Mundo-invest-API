from pydantic import BaseModel, EmailStr, Field


class CriarClienteDTO(BaseModel):
    cliente_nome: str = Field(..., min_length=1, description="Nome completo do cliente")
    cliente_email: EmailStr = Field(..., description="Email válido do cliente")
    tipo_solicitacao: str = Field(..., min_length=1, description="Tipo da solicitação")
    valor_patrimonio: float = Field(..., ge=0, description="Patrimônio em reais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_nome": "João Silva",
                "cliente_email": "joao.silva@example.com",
                "tipo_solicitacao": "Atualização cadastral",
                "valor_patrimonio": 250000
            }
        }