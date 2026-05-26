# Mundo Invest - Sistema de Gerenciamento de Clientes

Sistema interno para gerenciar clientes e patrimônios investidos, com integração ao Pipefy via GraphQL.

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture**:

- **Domain**: Entidades e regras de negócio puras
- **Application**: Casos de uso e interfaces
- **Infrastructure**: Implementações concretas (banco, APIs externas)
- **Presentation**: Controllers e API REST

## 🚀 Como Rodar

### Com Docker (recomendado)

```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f api

# API disponível em: http://localhost:8000
# PgAdmin em: http://localhost:5050
```

### Localmente

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
make install

# Configurar .env
cp .env.example .env

# Rodar aplicação
make run
```

## 📚 Documentação da API

Após rodar, acesse:
- Swagger UI: http://localhost:8000/docs

## 🧪 Testes

```bash
# Rodar todos os testes
make test

# Testes com coverage
pytest --cov=src --cov-report=html

# Ver relatório
open htmlcov/index.html
```

## 📋 Endpoints

### POST /clientes
Cria um novo cliente e estrutura card do Pipefy.

**Request:**
```json
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:8000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

**Response (201 Created):**
```json
{
  "sucesso": true,
  "mensagem": "Cliente cadastrado com sucesso",
  "cliente_id": 1,
  "status": "Aguardando Análise",
  "pipefy_mutation": {
    "mutation": "mutation CreateCard($input: CreateCardInput!) { ... }",
    "variables": { "input": { "pipe_id": "...", "title": "Cliente: João Silva", ... } }
  }
}
```

---

### GET /clientes
Lista todos os clientes cadastrados.

**Exemplo com curl:**
```bash
curl -X GET http://localhost:8000/clientes/
```

**Response (200 OK):**
```json
{
  "total": 2,
  "clientes": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao.silva@example.com",
      "tipo_solicitacao": "Atualização cadastral",
      "valor_patrimonio": 250000,
      "status": "Aguardando Análise",
      "prioridade": "ALTA"
    }
  ]
}
```

---

### POST /webhooks/pipefy/card-updated
Processa notificação de atualização do Pipefy.

**Request:**
```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_'$(date +%s)'",
    "card_id": "card_abc123",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "'$(date -u +'%Y-%m-%dT%H:%M:%SZ')'"
  }'
```

**Response (200 OK):**
```json
{
  "sucesso": true,
  "mensagem": "Webhook processado com sucesso",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "ALTA",
  "pipefy_mutation": {
    "sucesso": true,
    "atualizacoes": [
      {
        "tipo": "status",
        "mutation": "mutation UpdateCardField($input: UpdateCardFieldInput!) { ... }",
        "variables": { "input": { "card_id": "card_456", "field_id": "status_field_id", "new_value": "Processado" } }
      },
      {
        "tipo": "prioridade",
        "mutation": "mutation UpdateCardField($input: UpdateCardFieldInput!) { ... }",
        "variables": { "input": { "card_id": "card_456", "field_id": "prioridade_field_id", "new_value": "ALTA" } }
      }
    ]
  }
}
```

## 🔧 Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL / SQLite
- Pydantic
- Pytest
- Docker

## 📦 Estrutura do Projeto

```
src/
├── domain/                  # Entidades e regras de negócio
│   ├── entities/           # Cliente, EventoWebhook
│   ├── enums/              # StatusCliente, Prioridade
│   └── exceptions/         # Exceções de domínio
├── application/            # Casos de uso
│   ├── use_cases/          # CriarClienteUseCase, ProcessarWebhookUseCase
│   ├── dtos/               # Data Transfer Objects
│   └── interfaces/         # Abstrações (Repository, Gateway)
├── infrastructure/         # Implementações concretas
│   ├── database/           # SQLAlchemy models, conexão
│   └── external/           # PipefyGatewayImpl (GraphQL)
└── presentation/           # API e UI
    ├── api/                # FastAPI routes, main.py
    ├── routes/             # Endpoints (clientes, webhooks)
    ├── schemas/            # Pydantic models
    └── static/             # HTML/CSS/JS frontend

tests/
├── unit/                   # Testes unitários
├── integration/            # Testes de integração
└── e2e/                    # Testes ponta-a-ponta
```

## 🚀 Visão de Produção (AWS)

Para escalar essa arquitetura em produção na AWS, a estrutura seria a seguinte:

### **Componentes na AWS:**

1. **API Gateway + Lambda (Compute)**
   - Substituir FastAPI rodando em servidor por AWS Lambda
   - API Gateway gerencia autenticação, rate limiting e roteamento
   - Cada endpoint (`POST /clientes`, `POST /webhooks/pipefy/card-updated`) seria uma Lambda Function
   - Benefício: Escalabilidade automática, pagamento por uso

2. **RDS (Relational Database Service)**
   - Substituir PostgreSQL local por RDS PostgreSQL gerenciado
   - Backups automáticos, Multi-AZ para alta disponibilidade
   - Monitoring nativo com CloudWatch
   - Connection pooling via RDS Proxy para otimizar Lambda

3. **DynamoDB (Alternativa para Cache/Idempotência)**
   - Armazenar histórico de `event_id` processados para idempotência
   - TTL automático para limpeza de eventos antigos (após 24h, por exemplo)
   - Mais rápido que consultar PostgreSQL para validação de duplicata

4. **SQS (Processamento Assíncrono)**
   - Fila para processar webhooks do Pipefy
   - Lambda consome mensagens da fila e processa clientes
   - Desacopla recebimento de webhook do processamento
   - Retry automático em caso de falha

5. **CloudWatch (Logging e Monitoring)**
   - Logs centralizados de todas as Lambda Functions
   - Métricas de performance, erros e latência
   - Alertas conforme limiares configurados
   - Distribuição de logs em CloudWatch Logs

6. **SNS (Notificações)**
   - Publicar eventos de criação/atualização de clientes
   - Time comercial pode se inscrever para receber notificações
   - Integração com e-mail ou Slack

### **Fluxo de Produção:**

```
Pipefy (Webhook)
    ↓
API Gateway
    ↓
Lambda: ProcessarWebhook
    ↓
SQS (Fila)
    ↓
Lambda: ProcessarWebhookAsync
    ├→ RDS (Atualizar cliente)
    ├→ DynamoDB (Registrar event_id)
    └→ SNS (Notificar)
```

### **Benefícios:**

- **Escalabilidade**: Automática via Lambda (concorrência ilimitada)
- **Confiabilidade**: RDS Multi-AZ, backup automático
- **Idempotência**: DynamoDB + TTL garante processamento único
- **Observabilidade**: CloudWatch centraliza logs e métricas
- **Custo**: Pagamento apenas pelo tempo de execução (Lambda) e dados armazenados
- **Sem Gerenciamento**: AWS gerencia patches, atualizações e infraestrutura

