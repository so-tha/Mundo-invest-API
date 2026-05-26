from typing import Dict, Any
from ...application.interfaces.pipefy_gateway import IPipefyGateway


class PipefyGatewayImpl(IPipefyGateway):
    
    async def criar_card(
        self,
        nome: str,
        email: str,
        tipo_solicitacao: str,
        valor_patrimonio: float
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
                "pipe_id": "PIPE_ID_AQUI", 
                "title": f"Cliente: {nome}",
                "fields_attributes": [
                    {"field_id": "email_field_id", "field_value": email},
                    {"field_id": "tipo_field_id", "field_value": tipo_solicitacao},
                    {"field_id": "patrimonio_field_id", "field_value": str(valor_patrimonio)}
                ]
            }
        }
        
        return {
            "sucesso": True,
            "mutation": mutation,
            "variables": variables,
            "nota": "Mutation estruturada mas não enviada."
        }
    
    async def atualizar_card(
        self,
        card_id: str,
        status: str,
        prioridade: str
    ) -> Dict[str, Any]:
        
        mutation_status = """
        mutation UpdateCardFieldStatus($input: UpdateCardFieldInput!) {
          updateCardField(input: $input) {
            card {
              id
              fields {
                name
                value
              }
            }
            success
          }
        }
        """
        
        variables_status = {
            "input": {
                "card_id": card_id,
                "field_id": "status_field_id",  
                "new_value": status
            }
        }
  
        mutation_prioridade = """
        mutation UpdateCardFieldPrioridade($input: UpdateCardFieldInput!) {
          updateCardField(input: $input) {
            card {
              id
              fields {
                name
                value
              }
            }
            success
          }
        }
        """
        
        variables_prioridade = {
            "input": {
                "card_id": card_id,
                "field_id": "prioridade_field_id",  
                "new_value": prioridade
            }
        }
        
        return {
            "sucesso": True,
            "atualizacoes": [
                {
                    "tipo": "status",
                    "mutation": mutation_status,
                    "variables": variables_status,
                    "descricao": f"Atualiza status do card para '{status}'"
                },
                {
                    "tipo": "prioridade",
                    "mutation": mutation_prioridade,
                    "variables": variables_prioridade,
                    "descricao": f"Atualiza prioridade do card para '{prioridade}'"
                }
            ],
            "nota": "Mutations estruturadas conforme Pipefy API.",
            "exemple_payload": {
                "query": mutation_status,
                "variables": variables_status
            }
        }