def get_ui_html() -> str:
    """Retorna o HTML completo com CSS e JS inline"""
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mundo Invest API</title>
    <style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-black: #1a1a1a;
    --primary-white: #ffffff;
    --light-gray: #f5f5f5;
    --medium-gray: #e0e0e0;
    --dark-gray: #333333;
    --text-dark: #1a1a1a;
    --border-color: #e0e0e0;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.15);
}

html { scroll-behavior: smooth; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background-color: var(--light-gray);
    color: var(--text-dark);
    line-height: 1.6;
}

.header {
    background-color: var(--primary-black);
    color: var(--primary-white);
    padding: 2rem 0;
    box-shadow: var(--shadow-lg);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.logo h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

.logo p {
    font-size: 0.9rem;
    opacity: 0.9;
}

.status-indicator {
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
    background-color: var(--dark-gray);
    border-radius: 20px;
}

.status-indicator.healthy { background-color: #0d7313; }
.status-indicator.error { background-color: #c1121f; }

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.main { padding: 2rem 0; }

.card {
    background-color: var(--primary-white);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
    transition: box-shadow 0.3s ease;
}

.card:hover { box-shadow: var(--shadow-lg); }

.card h2 {
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    color: var(--primary-black);
    border-bottom: 2px solid var(--light-gray);
    padding-bottom: 0.75rem;
}

.card h3 {
    margin: 1rem 0 0.5rem 0;
    font-size: 1.1rem;
}

.form-group {
    margin-bottom: 1.25rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--text-dark);
    font-size: 0.95rem;
}

input, select, textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: var(--primary-black);
    box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.1);
}

input::placeholder { color: #999; }

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
}

.btn-primary {
    background-color: var(--primary-black);
    color: var(--primary-white);
}

.btn-primary:hover {
    background-color: var(--dark-gray);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.btn-secondary {
    background-color: var(--medium-gray);
    color: var(--text-dark);
}

.btn-secondary:hover { background-color: #d0d0d0; }

.btn-warning {
    background-color: #555555;
    color: var(--primary-white);
}

.btn-warning:hover { background-color: #666666; }

.table-container { overflow-x: auto; }

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

thead { background-color: var(--light-gray); }

th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid var(--medium-gray);
    color: var(--text-dark);
}

td {
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
}

tr:hover { background-color: #fafafa; }

.badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.badge-aguardando { background-color: #fff4e6; color: #cc8800; }
.badge-processado { background-color: #e8f5e9; color: #2e7d32; }
.badge-alta { background-color: #ffebee; color: #c62828; }
.badge-normal { background-color: #e3f2fd; color: #1565c0; }

.tabs {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.tab-btn {
    padding: 0.75rem 1.25rem;
    background-color: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    cursor: pointer;
    font-weight: 600;
    color: var(--text-dark);
    transition: all 0.3s ease;
}

.tab-btn.active {
    border-bottom-color: var(--primary-black);
    color: var(--primary-black);
}

.tab-btn:hover:not(.active) { color: #666; }

.tab-content {
    display: none;
}

.tab-content.active { display: block; }

.response-box {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 4px;
    border-left: 4px solid;
}

.response-box.hidden { display: none; }
.response-box.success { background-color: #e8f5e9; border-left-color: #2e7d32; color: #1b5e20; }
.response-box.error { background-color: #ffebee; border-left-color: #c62828; color: #b71c1c; }
.response-box.warning { background-color: #fff4e6; border-left-color: #e65100; color: #bf360c; }

.response-box pre {
    background-color: var(--primary-white);
    padding: 0.75rem;
    border-radius: 4px;
    margin-top: 0.5rem;
    overflow-x: auto;
    border: 1px solid var(--border-color);
}

.response-box code {
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
}

pre {
    background-color: #f5f5f5;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 1rem;
    overflow-x: auto;
    margin: 1rem 0;
}

code {
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    color: #333;
}

.mutation-desc {
    font-size: 0.85rem;
    color: #666;
    margin-top: 1rem;
}

.mutation-desc code {
    background-color: var(--light-gray);
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
}

.info-box {
    background-color: var(--light-gray);
    padding: 1rem;
    border-radius: 4px;
    border-left: 4px solid var(--primary-black);
}

.info-box p { margin-bottom: 0.75rem; }

.info-box a {
    color: var(--primary-black);
    text-decoration: none;
    font-weight: 600;
    border-bottom: 1px solid var(--medium-gray);
}

.info-box a:hover { border-bottom-color: var(--primary-black); }

.loading {
    text-align: center;
    padding: 2rem;
    color: #666;
}

.spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid var(--medium-gray);
    border-top-color: var(--primary-black);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.footer {
    background-color: var(--primary-black);
    color: var(--primary-white);
    text-align: center;
    padding: 2rem;
    margin-top: 4rem;
}

.footer p { opacity: 0.9; }

@media (max-width: 768px) {
    .header .container { flex-direction: column; gap: 1rem; }
    .card { padding: 1.5rem; }
    .tabs { flex-wrap: wrap; }
    table { font-size: 0.9rem; }
    th, td { padding: 0.75rem 0.5rem; }
}

@media (max-width: 480px) {
    .card h2 { font-size: 1.25rem; }
    .btn { width: 100%; padding: 0.9rem; }
    .form-group { margin-bottom: 1rem; }
}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <h1>Mundo Invest</h1>
                <p>Sistema de Gerenciamento de Clientes</p>
            </div>
            <div class="status-api">
                <span id="api-status" class="status-indicator">⚠️ Verificando...</span>
            </div>
        </div>
    </header>

    <main class="container main">
        <section class="card">
            <h2>📝 Criar Novo Cliente</h2>
            <form id="form-cliente">
                <div class="form-group">
                    <label for="nome">Nome Completo *</label>
                    <input type="text" id="nome" name="nome" required placeholder="João Silva">
                </div>

                <div class="form-group">
                    <label for="email">Email *</label>
                    <input type="email" id="email" name="email" required placeholder="joao@example.com">
                </div>

                <div class="form-group">
                    <label for="tipo">Tipo de Solicitação *</label>
                    <select id="tipo" name="tipo" required>
                        <option value="">Selecione...</option>
                        <option value="Atualização cadastral">Atualização cadastral</option>
                        <option value="Nova aplicação">Nova aplicação</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="patrimonio">Valor do Patrimônio (R$) *</label>
                    <input type="number" id="patrimonio" name="patrimonio" required min="0" placeholder="250000" step="1000">
                </div>

                <button type="submit" class="btn btn-primary">Criar Cliente</button>
            </form>
            <div id="response-create" class="response-box hidden"></div>
        </section>

        <section class="card">
            <h2>👥 Clientes Cadastrados</h2>
            <button id="btn-refresh" class="btn btn-secondary">🔄 Atualizar Lista</button>
            <div id="clientes-container" class="table-container">
                <p class="loading">Carregando clientes...</p>
            </div>
        </section>

        <section class="card">
            <h2>🔔 Simular Webhook do Pipefy</h2>
            <div class="form-group">
                <label for="webhook-email">Email do Cliente *</label>
                <input type="email" id="webhook-email" placeholder="joao@example.com">
            </div>
            <button id="btn-webhook" class="btn btn-warning">Disparar Webhook</button>
            <div id="response-webhook" class="response-box hidden"></div>
        </section>

        <section class="card">
            <h2>📊 GraphQL Mutations do Pipefy</h2>
            <div class="tabs">
                <button class="tab-btn active" data-tab="createcard">createCard</button>
                <button class="tab-btn" data-tab="updatecard">updateCardField</button>
            </div>
            
            <div id="createcard" class="tab-content active">
                <h3>Mutation: Criar Card (Cliente Novo)</h3>
                <p class="mutation-desc">✅ Estrutura real para criar um novo card no Pipefy com dados do cliente</p>
                
                <h4>GraphQL Mutation:</h4>
                <pre><code>mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
      fields {
        name
        value
      }
    }
    clientMutationId
  }
}</code></pre>

                <h4>Variables (Exemplo):</h4>
                <pre><code>{
  "input": {
    "pipe_id": "seu_pipe_id_aqui",
    "title": "Cliente: João Silva",
    "fields_attributes": [
      {
        "field_id": "email_field_id",
        "field_value": "joao@example.com"
      },
      {
        "field_id": "tipo_field_id",
        "field_value": "Nova aplicação"
      },
      {
        "field_id": "patrimonio_field_id",
        "field_value": "250000.0"
      }
    ]
  }
}</code></pre>

                <h4>Return Fields:</h4>
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                  <li><strong>card.id</strong> - ID único do card criado no Pipefy</li>
                  <li><strong>card.title</strong> - Título do card</li>
                  <li><strong>card.fields</strong> - Array de campos preenchidos</li>
                  <li><strong>clientMutationId</strong> - ID da transação (para tracking)</li>
                </ul>
                
                <p class="mutation-desc">📍 Localizado em: <code>src/infrastructure/external/pipefy_gateway_impl.py:7</code></p>
                <p class="mutation-desc">🔗 Chamado por: <code>src/application/use_cases/create_client_use_case.py:40</code> (POST /clientes)</p>
                <p class="mutation-desc">📖 Ref: https://api-docs.pipefy.com/reference/mutations/createCard/</p>
            </div>

            <div id="updatecard" class="tab-content">
                <h3>Mutation: Atualizar Card (Status + Prioridade)</h3>
                <p class="mutation-desc">✅ Estrutura real para atualizar o status ("Processado") e prioridade ("ALTA"/"NORMAL") no Pipefy</p>
                
                <h4>Atualizar Status:</h4>
                <pre><code>mutation UpdateCardFieldStatus($input: UpdateCardFieldInput!) {
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

Variables:
{
  "input": {
    "card_id": "card_12345",
    "field_id": "status_field_id",
    "new_value": "Processado"
  }
}</code></pre>

                <h4>Atualizar Prioridade:</h4>
                <pre><code>{
  "input": {
    "card_id": "card_12345",
    "field_id": "prioridade_field_id",
    "new_value": "ALTA"  // ou "NORMAL" se patrimônio < 200k
  }
}</code></pre>
                
                <p class="mutation-desc">📍 Localizado em: <code>src/application/use_cases/process_webhook_use_case.py:60</code> (linha onde chama pipefy_gateway.atualizar_card)</p>
                <p class="mutation-desc">🔗 Definição: <code>src/infrastructure/external/pipefy_gateway_impl.py:55</code></p>
            </div>
        </section>

        <section class="card">
            <h2>📋 Exemplos de Payload</h2>
            <div class="tabs">
                <button class="tab-btn active" data-tab="payload-create">POST /clientes</button>
                <button class="tab-btn" data-tab="payload-webhook">POST /webhooks/pipefy/card-updated</button>
            </div>

            <div id="payload-create" class="tab-content active">
                <h3>Criar Cliente</h3>
                <pre><code>{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}</code></pre>
            </div>

            <div id="payload-webhook" class="tab-content">
                <h3>Webhook do Pipefy</h3>
                <pre><code>{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-25T12:00:00Z"
}</code></pre>
            </div>
        </section>

        <section class="card">
            <h2>ℹ️ Informações</h2>
            <div class="info-box">
                <p><strong>Swagger UI:</strong> <a href="/docs" target="_blank">http://localhost:8000/docs</a></p>
                <p><strong>Health Check:</strong> <a href="/health" target="_blank">http://localhost:8000/health</a></p>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>Mundo Invest API</p>
    </footer>

    <script>
const API_BASE = '';

async function apiCall(method, path, data = null) {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (data) options.body = JSON.stringify(data);
    try {
        const response = await fetch(`${API_BASE}${path}`, options);
        if (!response.ok && response.status === 0) {
            throw new Error('Erro de conexão com a API. Verifique se o servidor está rodando.');
        }
        const json = await response.json();
        return { ok: response.ok, status: response.status, data: json };
    } catch (error) {
        console.error('API Error:', error);
        return { ok: false, status: 0, data: { error: error.message } };
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
}

function getStatusBadgeClass(status) {
    if (status.includes('Aguardando')) return 'badge-aguardando';
    if (status.includes('Processado')) return 'badge-processado';
    return 'badge-aguardando';
}

function getPriorityBadgeClass(priority) {
    if (!priority) return 'badge-normal';
    if (priority.includes('Alta')) return 'badge-alta';
    return 'badge-normal';
}

function showResponse(elementId, success, message, data = null) {
    const element = document.getElementById(elementId);
    element.classList.remove('hidden', 'success', 'error', 'warning');
    element.classList.add(success ? 'success' : 'error');
    let html = `<strong>${success ? '✅ Sucesso!' : '❌ Erro'}</strong><br>${message}`;
    if (data) html += `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;
    element.innerHTML = html;
}

async function checkApiHealth() {
    const statusElement = document.getElementById('api-status');
    try {
        const result = await apiCall('GET', '/health');
        if (result.ok) {
            statusElement.textContent = '✅ API Online';
            statusElement.classList.add('healthy');
        } else {
            statusElement.textContent = '⚠️ API Offline';
            statusElement.classList.add('error');
        }
    } catch (error) {
        statusElement.textContent = '❌ API Indisponível';
        statusElement.classList.add('error');
    }
}

async function handleCreateClient(e) {
    e.preventDefault();
    const formData = {
        cliente_nome: document.getElementById('nome').value,
        cliente_email: document.getElementById('email').value,
        tipo_solicitacao: document.getElementById('tipo').value,
        valor_patrimonio: parseInt(document.getElementById('patrimonio').value)
    };
    const result = await apiCall('POST', '/clientes/', formData);
    if (result.ok) {
        showResponse('response-create', true, `✅ Cliente criado com sucesso! ID: ${result.data.cliente_id}`, result.data);
        document.getElementById('form-cliente').reset();
        loadClients();
    } else {
        showResponse('response-create', false, `❌ Erro ao criar cliente: ${result.data.detail || result.data.error}`, result.data);
    }
}

async function handleWebhook() {
    const email = document.getElementById('webhook-email').value.trim();
    if (!email) {
        showResponse('response-webhook', false, 'Por favor, preencha o email do cliente');
        return;
    }
    const webhook_data = {
        event_id: `evt_${Date.now()}`,
        card_id: `card_${Math.random().toString(36).substr(2, 9)}`,
        cliente_email: email,
        timestamp: new Date().toISOString()
    };
    const result = await apiCall('POST', '/webhooks/pipefy/card-updated', webhook_data);
    if (result.ok) {
        const message = result.data.duplicado ? `⚠️ Evento duplicado: ${result.data.mensagem}` : `✅ Webhook processado com sucesso!`;
        showResponse('response-webhook', true, message, result.data);
        loadClients();
    } else {
        const errorMsg = result.data.detail || result.data.mensagem || result.data.error;
        showResponse('response-webhook', false, `❌ Erro ao processar webhook: ${errorMsg}`, result.data);
    }
}

async function loadClients() {
    const container = document.getElementById('clientes-container');
    container.innerHTML = '<p class="loading"><span class="spinner"></span> Carregando...</p>';
    const result = await apiCall('GET', '/clientes/');
    if (result.ok && result.data.total > 0) {
        let html = '<table><thead><tr><th>ID</th><th>Nome</th><th>Email</th><th>Tipo</th><th>Patrimônio</th><th>Status</th><th>Prioridade</th></tr></thead><tbody>';
        result.data.clientes.forEach(cliente => {
            const statusClass = getStatusBadgeClass(cliente.status);
            const priorityText = cliente.prioridade ? cliente.prioridade.replace('prioridade_', '') : '—';
            const priorityClass = getPriorityBadgeClass(cliente.prioridade);
            html += `<tr><td>${cliente.id}</td><td><strong>${cliente.nome}</strong></td><td>${cliente.email}</td><td>${cliente.tipo_solicitacao}</td><td>${formatCurrency(cliente.valor_patrimonio)}</td><td><span class="badge ${statusClass}">${cliente.status}</span></td><td><span class="badge ${priorityClass}">${priorityText}</span></td></tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    } else if (result.ok) {
        container.innerHTML = '<p style="text-align: center; color: #999;">Nenhum cliente cadastrado</p>';
    } else {
        container.innerHTML = '<p style="text-align: center; color: #c62828;">❌ Erro ao carregar clientes</p>';
    }
}

function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            const allContents = document.querySelectorAll('.tab-content');
            const allButtons = document.querySelectorAll('.tab-btn');
            allContents.forEach(content => content.classList.remove('active'));
            allButtons.forEach(btn => btn.classList.remove('active'));
            const content = document.getElementById(tabName);
            if (content) {
                content.classList.add('active');
                button.classList.add('active');
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    checkApiHealth();
    setInterval(checkApiHealth, 30000);
    loadClients();
    document.getElementById('form-cliente').addEventListener('submit', handleCreateClient);
    document.getElementById('btn-webhook').addEventListener('click', handleWebhook);
    document.getElementById('btn-refresh').addEventListener('click', loadClients);
    setupTabs();
});
    </script>
</body>
</html>"""
