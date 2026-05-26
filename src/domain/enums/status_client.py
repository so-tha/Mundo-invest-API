from enum import Enum

class StatusCliente(str, Enum):
    AGUARDANDO_ANALISE = "Aguardando Análise"
    PROCESSADO = "Processado"
    CANCELADO = "Cancelado"