"""
Gateway do Pipefy — suporta dois modos:

  - Modo Stub (padrão, sem token):
    Gera e retorna as mutations GraphQL sem enviá-las à API.
    Útil para desenvolvimento local e demonstração.

  - Modo Real (com PIPEFY_API_TOKEN configurado):
    Envia as mutations via HTTP para https://api.pipefy.com/graphql.
"""
import logging
from typing import Dict, Any, Optional

import httpx

from ...application.interfaces.pipefy_gateway import IPipefyGateway

logger = logging.getLogger(__name__)


class PipefyGatewayImpl(IPipefyGateway):
    """
    Implementação do gateway Pipefy.

    Quando `api_token` é fornecido, realiza chamadas HTTP reais à API GraphQL
    do Pipefy. Caso contrário, opera em modo stub: estrutura as mutations e
    as retorna sem enviá-las, permitindo desenvolvimento sem credenciais.
    """

    PIPEFY_URL = "https://api.pipefy.com/graphql"

    def __init__(self, api_token: Optional[str] = None, pipe_id: Optional[str] = None):
        self._api_token = api_token
        self._pipe_id = pipe_id or "PIPE_ID_AQUI"
        self._is_stub = api_token is None
        if self._is_stub:
            logger.info(
                "PipefyGateway iniciado em modo STUB "
                "(sem PIPEFY_API_TOKEN — mutations não são enviadas)"
            )

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json",
        }

    async def criar_card(
        self,
        nome: str,
        email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float,
    ) -> Dict[str, Any]:

        mutation = """
        mutation CreateCard($input: CreateCardInput!) {
          createCard(input: $input) {
            card {
              id
              title
              fields {
                id
                name
                value
              }
            }
            clientMutationId
          }
        }
        """

        variables = {
            "input": {
                "pipe_id": self._pipe_id,
                "title": f"Cliente: {nome}",
                "fields_attributes": [
                    {"field_id": "email_field_id", "field_value": email},
                    {"field_id": "tipo_field_id", "field_value": tipo_solicitacao},
                    {"field_id": "patrimonio_field_id", "field_value": str(valor_patrimonio)},
                ],
            }
        }

        if self._is_stub:
            logger.debug(f"[STUB] criar_card para '{nome}' — mutation estruturada, não enviada.")
            return {"sucesso": True, "modo": "stub", "mutation": mutation, "variables": variables}

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                self.PIPEFY_URL,
                json={"query": mutation, "variables": variables},
                headers=self._headers,
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"✓ Card criado no Pipefy para '{nome}'")
            return {"sucesso": True, "modo": "real", "data": data}

    async def atualizar_card(
        self,
        card_id: str,
        status: str,
        prioridade: str,
    ) -> Dict[str, Any]:

        mutation_status = """
        mutation UpdateCardFieldStatus($input: UpdateCardFieldInput!) {
          updateCardField(input: $input) {
            card { id fields { name value } }
            success
          }
        }
        """

        mutation_prioridade = """
        mutation UpdateCardFieldPrioridade($input: UpdateCardFieldInput!) {
          updateCardField(input: $input) {
            card { id fields { name value } }
            success
          }
        }
        """

        updates = [
            {
                "tipo": "status",
                "mutation": mutation_status,
                "variables": {
                    "input": {
                        "card_id": card_id,
                        "field_id": "status_field_id",
                        "new_value": status,
                    }
                },
            },
            {
                "tipo": "prioridade",
                "mutation": mutation_prioridade,
                "variables": {
                    "input": {
                        "card_id": card_id,
                        "field_id": "prioridade_field_id",
                        "new_value": prioridade,
                    }
                },
            },
        ]

        if self._is_stub:
            logger.debug(f"[STUB] atualizar_card '{card_id}' — mutations estruturadas, não enviadas.")
            return {"sucesso": True, "modo": "stub", "atualizacoes": updates}

        resultados = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for update in updates:
                response = await client.post(
                    self.PIPEFY_URL,
                    json={"query": update["mutation"], "variables": update["variables"]},
                    headers=self._headers,
                )
                response.raise_for_status()
                resultados.append({"tipo": update["tipo"], "data": response.json()})

        logger.info(f"✓ Card '{card_id}' atualizado no Pipefy")
        return {"sucesso": True, "modo": "real", "atualizacoes": resultados}