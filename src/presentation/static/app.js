/**
 * Aplicação web para gerenciar clientes Mundo Invest
 * Integração com API de criação de clientes e webhooks do Pipefy
 */

const API_BASE = 'http://localhost:8000';

async function apiCall(method, path, data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE}${path}`, options);
        const json = await response.json();
        return { ok: response.ok, status: response.status, data: json };
    } catch (error) {
        return { ok: false, status: 0, data: { error: error.message } };
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function getStatusBadgeClass(status) {
    if (status.includes('Aguardando')) return 'badge-aguardando';
    if (status.includes('Processado')) return 'badge-processado';
    return 'badge-aguardando';
}

function getPriorityBadgeClass(priority) {
    if (!priority) return 'badge-normal';
    if (priority.includes('alta')) return 'badge-alta';
    return 'badge-normal';
}

function showResponse(elementId, success, message, data = null) {
    const element = document.getElementById(elementId);
    element.classList.remove('hidden', 'success', 'error', 'warning');
    element.classList.add(success ? 'success' : 'error');

    let html = `<strong>${success ? '✅ Sucesso!' : '❌ Erro'}</strong><br>${message}`;

    if (data) {
        html += `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;
    }

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

// ============================================
// Form Handlers
// ============================================

async function handleCreateClient(e) {
    e.preventDefault();

    const formData = {
        cliente_nome: document.getElementById('nome').value,
        cliente_email: document.getElementById('email').value,
        tipo_solicitacao: 'Nova aplicação',
        valor_patrimonio: parseInt(document.getElementById('patrimonio').value)
    };

    const result = await apiCall('POST', '/clientes/', formData);

    if (result.ok) {
        showResponse(
            'response-create',
            true,
            `Cliente criado com sucesso! ID: ${result.data.cliente_id}`,
            result.data
        );
        document.getElementById('form-cliente').reset();
        loadClients(); 
    } else {
        showResponse(
            'response-create',
            false,
            `Erro ao criar cliente: ${result.data.detail || result.data.error}`,
            result.data
        );
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
        const message = result.data.duplicado
            ? `Evento duplicado: ${result.data.mensagem}`
            : `Webhook processado com sucesso!`;

        showResponse('response-webhook', true, message, result.data);
        loadClients();
    } else {
        const errorMsg = result.data.detail || result.data.mensagem || result.data.error;
        showResponse(
            'response-webhook',
            false,
            `❌ Erro ao processar webhook: ${errorMsg}`,
            result.data
        );
    }
}

async function loadClients() {
    const container = document.getElementById('clientes-container');
    container.innerHTML = '<p class="loading"><span class="spinner"></span> Carregando...</p>';

    const result = await apiCall('GET', '/clientes/');

    if (result.ok && result.data.total > 0) {
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Tipo</th>
                        <th>Patrimônio</th>
                        <th>Status</th>
                        <th>Prioridade</th>
                    </tr>
                </thead>
                <tbody>
        `;

        result.data.clientes.forEach(cliente => {
            const statusClass = getStatusBadgeClass(cliente.status);
            const statusDisplay = cliente.status === 'Processado' ? 'Novo Cliente' : cliente.status;
            const priorityText = cliente.prioridade 
                ? cliente.prioridade.replace('prioridade_', '').charAt(0).toUpperCase() + cliente.prioridade.replace('prioridade_', '').slice(1)
                : '—';
            const priorityClass = getPriorityBadgeClass(cliente.prioridade);

            html += `
                <tr>
                    <td>${cliente.id}</td>
                    <td><strong>${cliente.nome}</strong></td>
                    <td>${cliente.email}</td>
                    <td>${cliente.tipo_solicitacao}</td>
                    <td>${formatCurrency(cliente.valor_patrimonio)}</td>
                    <td><span class="badge ${statusClass}">${statusDisplay}</span></td>
                    <td><span class="badge ${priorityClass}">${priorityText}</span></td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        container.innerHTML = html;
    } else if (result.ok) {
        container.innerHTML = '<p style="text-align: center; color: #999;">Nenhum cliente cadastrado</p>';
    } else {
        container.innerHTML = '<p style="text-align: center; color: #c62828;">❌ Erro ao carregar clientes</p>';
    }
}

// ============================================
// Tab Navigation
// ============================================

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

// ============================================
// Event Listeners
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    checkApiHealth();
    setInterval(checkApiHealth, 30000);
    loadClients();

    document.getElementById('form-cliente').addEventListener('submit', handleCreateClient);
    document.getElementById('btn-webhook').addEventListener('click', handleWebhook);
    document.getElementById('btn-refresh').addEventListener('click', loadClients);

    setupTabs();
});
