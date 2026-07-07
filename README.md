# Mundo Invest — Sistema de Gerenciamento de Clientes

> API REST para gerenciamento de clientes e patrimônios investidos, com integração ao Pipefy via GraphQL.

![CI](https://github.com/SEU_USUARIO/Mundo-invest-API/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture**, garantindo que regras de negócio sejam completamente independentes de frameworks, banco de dados ou APIs externas:

```
src/
├── domain/           # Entidades, enums e exceções de negócio (zero dependências externas)
├── application/      # Casos de uso, DTOs e interfaces (depende só do domain)
├── infrastructure/   # Implementações concretas: banco, gateway Pipefy (depende de tudo)
└── presentation/     # FastAPI: rotas, schemas, dependencies (depende de application)
```

**Fluxo de uma requisição:**
```
HTTP Request → Route → UseCase → Repository/Gateway → Response
                         ↑
                    Domain Entity (regras de negócio)
```

## 🚀 Como Rodar

### Com Docker (recomendado)

```bash
# Copiar variáveis de ambiente
cp .env.example .env

# Subir todos os serviços (API + PostgreSQL + PgAdmin)
docker compose up -d

# Ver logs
docker compose logs -f api

# API disponível em: http://localhost:8000
# Swagger UI em:    http://localhost:8000/docs
# PgAdmin em:       http://localhost:5050
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

# Configurar variáveis
cp .env.example .env
# Edite .env com suas configurações

# Rodar aplicação
make run
```

## ⚙️ Configuração

Copie `.env.example` para `.env` e ajuste conforme necessário:

| Variável | Padrão | Descrição |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://...` | URL do banco de dados |
| `PIPEFY_API_TOKEN` | _(vazio)_ | Token Pipefy — se vazio, usa **modo stub** |
| `PIPEFY_PIPE_ID` | _(vazio)_ | ID do pipe no Pipefy |
| `API_KEY` | _(vazio)_ | Protege `POST /clientes` — se vazio, auth desabilitada |
| `CORS_ORIGINS` | `*` | Origens CORS permitidas (ex: `https://meusite.com`) |
| `ENVIRONMENT` | `development` | `development`, `production` ou `test` |

### Modo Stub do Pipefy

Quando `PIPEFY_API_TOKEN` não está configurado, o gateway opera em **modo stub**: as mutations GraphQL são montadas e retornadas na resposta, mas não são enviadas à API. Isso permite rodar e testar sem credenciais do Pipefy.

## 📚 Documentação da API

Após rodar, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Autenticação

Endpoints de escrita requerem o header `X-API-Key` quando `API_KEY` está configurada:

```bash
curl -H "X-API-Key: sua_chave_aqui" -X POST http://localhost:8000/clientes/ ...
```

## 🧪 Testes

```bash
# Rodar todos os testes
make test

# Testes com coverage
pytest --cov=src --cov-report=html

# Ver relatório de coverage
open htmlcov/index.html
```

## 📋 Endpoints

### POST /clientes
Cria um novo cliente e enfileira a criação do card no Pipefy.

Requer header `X-API-Key` quando `API_KEY` está configurada.

**Request:**
```json
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}
```

**Response (201 Created):**
```json
{
  "sucesso": true,
  "mensagem": "Cliente cadastrado com sucesso",
  "cliente_id": 1,
  "status": "Aguardando Análise",
  "pipefy_card_enqueued": true
}
```

**Erros:**
- `409 Conflict` — Email já cadastrado
- `400 Bad Request` — Dados inválidos (email mal formatado, patrimônio negativo)
- `403 Forbidden` — API Key inválida

---

### GET /clientes
Lista clientes com paginação.

```bash
# Página 1 (20 por página)
curl http://localhost:8000/clientes/

# Paginação customizada
curl "http://localhost:8000/clientes/?limit=10&offset=20"
```

**Response (200 OK):**
```json
{
  "sucesso": true,
  "total": 1,
  "limit": 20,
  "offset": 0,
  "clientes": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao.silva@example.com",
      "tipo_solicitacao": "Atualização cadastral",
      "valor_patrimonio": 250000,
      "status": "Aguardando Análise",
      "prioridade": null
    }
  ]
}
```

---

### POST /webhooks/pipefy/card-updated
Processa notificação de atualização do Pipefy. **Idempotente** — eventos duplicados retornam 200 sem reprocessamento.

**Request:**
```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

**Response (200 OK):**
```json
{
  "sucesso": true,
  "mensagem": "Webhook processado com sucesso",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "ALTA",
  "pipefy_mutation": { ... }
}
```

---

### GET /health
Verifica status da API e conexão com banco de dados.

```bash
curl http://localhost:8000/health
```

## 🔧 Tecnologias

| Camada | Tecnologia |
|---|---|
| Framework | FastAPI 0.109 + Uvicorn |
| Validação | Pydantic v2 |
| ORM | SQLAlchemy 2.0 (async) |
| Banco | PostgreSQL / SQLite |
| HTTP Client | httpx (gateway Pipefy) |
| Resiliência | tenacity (retry com backoff) |
| Testes | pytest + pytest-asyncio |
| Linting | black + flake8 + isort + mypy |
| Infra | Docker + docker-compose |
