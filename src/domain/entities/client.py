from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from ..enums import Prioridade, StatusCliente


@dataclass
class Cliente:
    """Entidade de domínio Cliente"""

    nome: str
    email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: StatusCliente
    prioridade: Optional[Prioridade] = None
    id: Optional[int] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    def __post_init__(self):
        self._validar()

    def _validar(self):
        if not self.nome or len(self.nome.strip()) == 0:
            raise ValueError("Nome do cliente é obrigatório")

        if not self.email or "@" not in self.email:
            raise ValueError("Email inválido")

        if self.valor_patrimonio < 0:
            raise ValueError("Patrimônio não pode ser negativo")

    def calcular_prioridade(self) -> Prioridade:
        if self.valor_patrimonio >= 200_000:
            return Prioridade.ALTA
        return Prioridade.NORMAL

    def processar(self):
        self.status = StatusCliente.PROCESSADO
        self.prioridade = self.calcular_prioridade()
        self.atualizado_em = datetime.now(timezone.utc)
