from pydantic import BaseModel, EmailStr
from datetime import datetime


class WebhookDTO(BaseModel):
    """DTO para processamento de webhook"""
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime