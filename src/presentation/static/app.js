/**
 * InvestHub — Dashboard Frontend
 * Premium fintech UI for the FastAPI backend
 */

const API_BASE = '';  // same origin (served by FastAPI)

// ─── State ───────────────────────────────────────────────────────────────────

let allClients = [];
let filteredClients = [];
let currentPage = 1;
const PAGE_SIZE = 10;

// ─── API Helper ──────────────────────────────────────────────────────────────

async function api(method, path, body = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  try {
    const res = await fetch(`${API_BASE}${path}`, opts);
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (err) {
    return { ok: false, status: 0, data: { error: err.message } };
  }
}

// ─── Formatters ──────────────────────────────────────────────────────────────

function currency(v) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v);
}

function statusBadge(status) {
  if (!status) return `<span class="badge badge-neutral">—</span>`;
  const cls = status.includes('Aguardando') ? 'badge-aguardando' : 'badge-processado';
  return `<span class="badge ${cls}">${status}</span>`;
}

function priorityBadge(p) {
  if (!p) return `<span class="badge badge-neutral">—</span>`;
  const label = p.replace('prioridade_', '');
  const cls = label.toLowerCase().includes('alta') ? 'badge-alta' : 'badge-normal';
  return `<span class="badge ${cls}">${label.charAt(0).toUpperCase() + label.slice(1)}</span>`;
}

// ─── Response Box ─────────────────────────────────────────────────────────────

function showResponse(id, success, message, data = null) {
  const el = document.getElementById(id);
  el.className = `response-box ${success ? 'success' : 'error'}`;
  let html = `<strong>${success ? '✅ ' : '❌ '}${message}</strong>`;
  if (data) html += `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;
  el.innerHTML = html;
}

// ─── API Health ───────────────────────────────────────────────────────────────

async function checkHealth() {
  const pill = document.getElementById('api-status');
  const label = pill.querySelector('.status-label');
  const r = await api('GET', '/health');
  if (r.ok && r.data.status === 'ok') {
    pill.className = 'api-status-pill online';
    label.textContent = 'API Online';
  } else {
    pill.className = 'api-status-pill offline';
    label.textContent = 'API Offline';
  }
}

// ─── Load Clients ─────────────────────────────────────────────────────────────

async function loadClients() {
  const r = await api('GET', '/clientes/?limit=100&offset=0');
  if (r.ok) {
    allClients = r.data.clientes || [];
    filteredClients = [...allClients];
    renderMetrics();
    renderClientsTable();
    renderDashboardRecent();
  }
}

// ─── Metrics ──────────────────────────────────────────────────────────────────

function renderMetrics() {
  const total = allClients.length;
  const patrimonio = allClients.reduce((s, c) => s + (c.valor_patrimonio || 0), 0);
  const aguardando = allClients.filter(c => c.status?.includes('Aguardando')).length;
  const processados = allClients.filter(c => c.status?.includes('Processado')).length;

  animateCount('metric-total-val', total, v => String(v));
  animateCount('metric-patrimonio-val', patrimonio, v => currency(v));
  animateCount('metric-aguardando-val', aguardando, v => String(v));
  animateCount('metric-processados-val', processados, v => String(v));
}

function animateCount(id, target, fmt) {
  const el = document.getElementById(id);
  if (!el) return;
  const start = 0;
  const duration = 700;
  const startTime = performance.now();

  function step(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (target - start) * eased);
    el.textContent = fmt(current);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// ─── Dashboard Recent ─────────────────────────────────────────────────────────

function renderDashboardRecent() {
  const container = document.getElementById('dashboard-clientes-container');
  const recent = allClients.slice(-5).reverse();

  if (recent.length === 0) {
    container.innerHTML = '<p class="empty-state">Nenhum cliente cadastrado ainda.</p>';
    return;
  }

  container.innerHTML = buildTable(recent);
}

// ─── Full Client Table ────────────────────────────────────────────────────────

function renderClientsTable() {
  const container = document.getElementById('clientes-container');
  if (!container) return;

  const start = (currentPage - 1) * PAGE_SIZE;
  const paged = filteredClients.slice(start, start + PAGE_SIZE);

  if (paged.length === 0) {
    container.innerHTML = '<p class="empty-state">Nenhum cliente encontrado.</p>';
    renderPagination(0);
    return;
  }

  container.innerHTML = buildTable(paged);
  renderPagination(filteredClients.length);
}

function buildTable(clients) {
  return `
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Nome</th>
          <th>Email</th>
          <th>Tipo</th>
          <th>Patrimônio</th>
          <th>Status</th>
          <th>Prioridade</th>
        </tr>
      </thead>
      <tbody>
        ${clients.map(c => `
          <tr>
            <td style="color:var(--text-muted);font-size:0.8rem">${c.id}</td>
            <td class="td-name">${escHtml(c.nome)}</td>
            <td class="td-email">${escHtml(c.email)}</td>
            <td style="color:var(--text-secondary);font-size:0.83rem">${escHtml(c.tipo_solicitacao)}</td>
            <td class="td-currency">${currency(c.valor_patrimonio)}</td>
            <td>${statusBadge(c.status)}</td>
            <td>${priorityBadge(c.prioridade)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function escHtml(s) {
  if (!s) return '—';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ─── Pagination ───────────────────────────────────────────────────────────────

function renderPagination(total) {
  const container = document.getElementById('pagination');
  if (!container) return;
  const pages = Math.ceil(total / PAGE_SIZE);
  if (pages <= 1) { container.innerHTML = ''; return; }

  let html = '';
  for (let i = 1; i <= pages; i++) {
    html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
  }
  container.innerHTML = html;

  container.querySelectorAll('.page-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentPage = parseInt(btn.dataset.page);
      renderClientsTable();
    });
  });
}

// ─── Search ───────────────────────────────────────────────────────────────────

function setupSearch() {
  const input = document.getElementById('search-input');
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    filteredClients = q
      ? allClients.filter(c =>
          (c.nome || '').toLowerCase().includes(q) ||
          (c.email || '').toLowerCase().includes(q)
        )
      : [...allClients];
    currentPage = 1;
    renderClientsTable();
  });
}

// ─── Create Client Form ───────────────────────────────────────────────────────

async function handleCreateClient(e) {
  e.preventDefault();

  const btn = document.getElementById('btn-submit');
  const btnText = btn.querySelector('.btn-text');
  const btnSpinner = btn.querySelector('.btn-spinner');

  // Set loading state
  btn.disabled = true;
  btnText.textContent = 'Enviando...';
  btnSpinner.classList.remove('hidden');

  const body = {
    cliente_nome: document.getElementById('nome').value.trim(),
    cliente_email: document.getElementById('email').value.trim(),
    tipo_solicitacao: document.getElementById('tipo').value,
    valor_patrimonio: parseFloat(document.getElementById('patrimonio').value),
  };

  const r = await api('POST', '/clientes/', body);

  btn.disabled = false;
  btnText.textContent = 'Cadastrar Cliente';
  btnSpinner.classList.add('hidden');

  if (r.ok) {
    showResponse('response-create', true, `Cliente #${r.data.cliente_id} cadastrado com sucesso!`, r.data);
    document.getElementById('form-cliente').reset();
    await loadClients();
  } else {
    const msg = r.data.detail || r.data.error || 'Erro desconhecido';
    showResponse('response-create', false, msg, r.data);
  }
}

// ─── Webhook Simulator ────────────────────────────────────────────────────────

function updatePayloadPreview() {
  const email = document.getElementById('webhook-email')?.value.trim() || 'cliente@exemplo.com';
  const payload = {
    event_id: `evt_${Date.now()}`,
    card_id: `card_${Math.random().toString(36).substr(2, 9)}`,
    cliente_email: email,
    timestamp: new Date().toISOString(),
  };
  const code = document.getElementById('payload-code');
  if (code) code.textContent = JSON.stringify(payload, null, 2);
  return payload;
}

async function handleWebhook() {
  const email = document.getElementById('webhook-email')?.value.trim();
  if (!email) {
    showResponse('response-webhook', false, 'Informe o e-mail do cliente.');
    return;
  }

  const payload = updatePayloadPreview();
  const btn = document.getElementById('btn-webhook');
  btn.disabled = true;
  btn.textContent = '⏳ Enviando...';

  const r = await api('POST', '/webhooks/pipefy/card-updated', payload);

  btn.disabled = false;
  btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg> Disparar Webhook`;

  if (r.ok) {
    const dup = r.data.duplicado;
    showResponse('response-webhook', true, dup ? 'Evento duplicado (idempotente).' : 'Webhook processado com sucesso!', r.data);
    await loadClients();
  } else {
    showResponse('response-webhook', false, r.data.detail || r.data.error || 'Erro ao processar.', r.data);
  }
}

// ─── Navigation ───────────────────────────────────────────────────────────────

const SECTIONS = ['dashboard', 'clientes', 'novo', 'webhook'];

function navigate(section) {
  SECTIONS.forEach(s => {
    document.getElementById(`section-${s}`)?.classList.remove('active');
    document.getElementById(`nav-${s}`)?.classList.remove('active');
  });

  document.getElementById(`section-${section}`)?.classList.add('active');
  document.getElementById(`nav-${section}`)?.classList.add('active');

  const titles = { dashboard: 'Dashboard', clientes: 'Clientes', novo: 'Novo Cliente', webhook: 'Webhooks' };
  const topbarTitle = document.getElementById('topbar-title');
  if (topbarTitle) topbarTitle.textContent = titles[section] || '';

  // Close sidebar on mobile
  if (window.innerWidth <= 768) {
    document.getElementById('sidebar')?.classList.remove('open');
  }

  if (section === 'clientes') {
    setupSearch();
    renderClientsTable();
  }
}

// ─── Tabs ─────────────────────────────────────────────────────────────────────

function setupTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      const parent = btn.closest('.card, .info-side');
      if (!parent) return;

      parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      parent.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      parent.querySelector(`#${tabId}`)?.classList.add('active');
    });
  });
}

// ─── Init ─────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // Sidebar nav
  SECTIONS.forEach(s => {
    document.getElementById(`nav-${s}`)?.addEventListener('click', e => {
      e.preventDefault();
      navigate(s);
    });
  });

  // Mobile menu toggle
  document.getElementById('menu-toggle')?.addEventListener('click', () => {
    document.getElementById('sidebar')?.classList.toggle('open');
  });

  // Refresh buttons
  document.getElementById('btn-refresh-top')?.addEventListener('click', loadClients);
  document.getElementById('btn-refresh-clientes')?.addEventListener('click', loadClients);

  // "Ver todos" on dashboard
  document.getElementById('btn-ver-todos')?.addEventListener('click', () => navigate('clientes'));

  // Form
  document.getElementById('form-cliente')?.addEventListener('submit', handleCreateClient);

  // Patrimônio hint
  document.getElementById('patrimonio')?.addEventListener('input', function () {
    const hint = document.getElementById('patrimonio-hint');
    if (hint && this.value) hint.textContent = currency(parseFloat(this.value) || 0);
    else if (hint) hint.textContent = '';
  });

  // Webhook
  document.getElementById('btn-webhook')?.addEventListener('click', handleWebhook);
  document.getElementById('webhook-email')?.addEventListener('input', updatePayloadPreview);
  updatePayloadPreview();

  // Tabs
  setupTabs();

  // Search (lazy — only when section is active)
  setupSearch();

  // Boot
  checkHealth();
  setInterval(checkHealth, 30_000);
  loadClients();

  // Start on dashboard
  navigate('dashboard');
});
