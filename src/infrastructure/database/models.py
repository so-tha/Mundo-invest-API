from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from ...domain.enums.status_client import StatusCliente
from ...domain.enums.priority import Prioridade

Base = declarative_base()


class ClienteModel(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    tipo_solicitacao = Column(String, nullable=False)
    valor_patrimonio = Column(Float, nullable=False)
    status = Column(Enum(StatusCliente), nullable=False)
    prioridade = Column(Enum(Prioridade), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())


class EventoWebhookModel(Base):
    __tablename__ = "eventos_webhook"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    card_id = Column(String, nullable=False)
    cliente_email = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    processado = Column(Boolean, default=False)
    processado_em = Column(DateTime(timezone=True), nullable=True)