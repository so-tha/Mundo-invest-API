import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....application.interfaces.client_repository import IClienteRepository
from ....domain.entities.client import Cliente
from ..models import ClienteModel

logger = logging.getLogger(__name__)


class ClienteRepositoryImpl(IClienteRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def criar(self, cliente: Cliente) -> Cliente:
        db_cliente = ClienteModel(
            nome=cliente.nome,
            email=cliente.email,
            tipo_solicitacao=cliente.tipo_solicitacao,
            valor_patrimonio=cliente.valor_patrimonio,
            status=cliente.status,
            prioridade=cliente.prioridade,
        )

        try:
            logger.info(f"Salvando cliente: {cliente.email}")
            self._session.add(db_cliente)
            await self._session.commit()
            logger.info(f" Commit realizado. ID antes refresh: {db_cliente.id}")

            await self._session.refresh(db_cliente)
            logger.info(f" Refresh concluído. ID final: {db_cliente.id}")

            return self._to_entity(db_cliente)
        except Exception as e:
            logger.error(f" Erro ao criar cliente: {str(e)}")
            await self._session.rollback()
            raise

    async def buscar_por_email(self, email: str) -> Optional[Cliente]:
        result = await self._session.execute(
            select(ClienteModel).where(ClienteModel.email == email)
        )
        db_cliente = result.scalar_one_or_none()

        if not db_cliente:
            return None

        return self._to_entity(db_cliente)

    async def atualizar(self, cliente: Cliente) -> Cliente:
        result = await self._session.execute(
            select(ClienteModel).where(ClienteModel.email == cliente.email)
        )
        db_cliente = result.scalar_one()

        db_cliente.status = cliente.status
        db_cliente.prioridade = cliente.prioridade
        db_cliente.atualizado_em = cliente.atualizado_em

        await self._session.commit()
        await self._session.refresh(db_cliente)

        return self._to_entity(db_cliente)

    async def listar_todos(self, limit: int = 20, offset: int = 0) -> list:
        result = await self._session.execute(
            select(ClienteModel).offset(offset).limit(limit)
        )
        db_clientes = result.scalars().all()

        return [self._to_entity(db_cliente) for db_cliente in db_clientes]

    @staticmethod
    def _to_entity(model: ClienteModel) -> Cliente:
        return Cliente(
            id=model.id,
            nome=model.nome,
            email=model.email,
            tipo_solicitacao=model.tipo_solicitacao,
            valor_patrimonio=model.valor_patrimonio,
            status=model.status,
            prioridade=model.prioridade,
            criado_em=model.criado_em,
            atualizado_em=model.atualizado_em,
        )
