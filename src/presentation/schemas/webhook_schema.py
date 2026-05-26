from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class WebhookRequest(BaseModel):
    event_id: str = Field(..., description="ID único do evento")
    card_id: str = Field(..., description="ID do card no Pipefy")
    cliente_email: EmailStr = Field(..., description="Email do cliente")
    timestamp: datetime = Field(..., description="Data/hora do evento")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "evt_123",
                "card_id": "card_456",
                "cliente_email": "joao.silva@example.com",
                "timestamp": "2026-05-18T12:00:00Z"
            }
        }


class WebhookResponse(BaseModel):
    sucesso: bool
    mensagem: str
    cliente_email: Optional[str] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    duplicado: bool = False
    pipefy_mutation: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "sucesso": True,
                "mensagem": "Webhook processado com sucesso",
                "cliente_email": "joao.silva@example.com",
                "status": "Processado",
                "prioridade": "prioridade_alta",
                "duplicado": False
            }
        }