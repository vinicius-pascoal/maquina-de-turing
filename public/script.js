// Estado global da aplicação
let currentMachine = null;
let examples = {};

// API Base URL (ajusta automaticamente para desenvolvimento/produção)
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? '/api'
  : '/api';

// Elementos DOM
const elements = {
  specEditor: document.getElementById('spec-editor'),
  inputField: document.getElementById('input-field'),
  examplesSelect: document.getElementById('examples-select'),
  validateBtn: document.getElementById('validate-btn'),
  resetBtn: document.getElementById('reset-btn'),
  stepBtn: document.getElementById('step-btn'),
  run10Btn: document.getElementById('run-10-btn'),
  runAllBtn: document.getElementById('run-all-btn'),
  validationMessage: document.getElementById('validation-message'),
  currentState: document.getElementById('current-state'),
  headPosition: document.getElementById('head-position'),
  currentSymbol: document.getElementById('current-symbol'),
  resultBadge: document.getElementById('result-badge'),
  tapeContainer: document.getElementById('tape-container'),
  transitionsTable: document.getElementById('transitions-table'),
  loadingOverlay: document.getElementById('loading-overlay')
};

// Utilitários
const showLoading = () => elements.loadingOverlay.classList.remove('hidden');
const hideLoading = () => elements.loadingOverlay.classList.add('hidden');

const showValidation = (message, isSuccess) => {
  elements.validationMessage.textContent = message;
  elements.validationMessage.className = `validation-message ${isSuccess ? 'success' : 'error'}`;
  setTimeout(() => {
    if (elements.validationMessage.textContent === message) {
      elements.validationMessage.textContent = '';
      elements.validationMessage.className = 'validation-message';
    }
  }, 5000);
};

// API Calls
async function apiCall(endpoint, data = null) {
  try {
    const options = {
      method: data ? 'POST' : 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE}/${endpoint}`, options);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Erro na requisição');
    }

    return result;
  } catch (error) {
    console.error(`Erro em ${endpoint}:`, error);
    throw error;
  }
}

// Carregar exemplos
async function loadExamples() {
  try {
    const response = await apiCall('examples');
    if (response.success) {
      examples = response.examples;
      populateExamplesSelect();
    }
  } catch (error) {
    console.error('Erro ao carregar exemplos:', error);
  }
}

function populateExamplesSelect() {
  elements.examplesSelect.innerHTML = '<option value="">Selecione um exemplo...</option>';
  Object.keys(examples).forEach(name => {
    const option = document.createElement('option');
    option.value = name;
    option.textContent = name;
    elements.examplesSelect.appendChild(option);
  });
}

// Validar especificação
async function validateSpec() {
  const spec = elements.specEditor.value.trim();

  if (!spec) {
    showValidation('Especificação vazia', false);
    return;
  }

  showLoading();
  try {
    const response = await apiCall('validate', { spec });

    if (response.success) {
      showValidation(`✓ ${response.message} (${response.states.length} estados, ${response.transitions_count} transições)`, true);
      updateTransitionsTable(spec);
    } else {
      showValidation(`✗ ${response.error}`, false);
    }
  } catch (error) {
    showValidation(`✗ Erro: ${error.message}`, false);
  } finally {
    hideLoading();
  }
}

// Resetar máquina
async function resetMachine() {
  const spec = elements.specEditor.value.trim();
  const input = elements.inputField.value;

  if (!spec) {
    showValidation('Digite uma especificação primeiro', false);
    return;
  }

  showLoading();
  try {
    const response = await apiCall('reset', { spec, input });

    if (response.success) {
      currentMachine = response.machine;
      updateUI();
      enableControls();
      showValidation('✓ Máquina inicializada!', true);
    } else {
      showValidation(`✗ ${response.error}`, false);
    }
  } catch (error) {
    showValidation(`✗ Erro: ${error.message}`, false);
  } finally {
    hideLoading();
  }
}

// Executar um passo
async function step() {
  if (!currentMachine) return;

  showLoading();
  try {
    const response = await apiCall('step', { machine: currentMachine });

    if (response.success) {
      currentMachine = response.machine;
      updateUI();

      if (currentMachine.halted) {
        disableControls();
      }
    }
  } catch (error) {
    showValidation(`✗ Erro: ${error.message}`, false);
  } finally {
    hideLoading();
  }
}

// Executar N passos
async function runSteps(steps) {
  if (!currentMachine) return;

  showLoading();
  try {
    const response = await apiCall('run', {
      machine: currentMachine,
      steps: steps,
      max_steps: 1000
    });

    if (response.success) {
      currentMachine = response.machine;
      updateUI();

      if (currentMachine.halted) {
        disableControls();
      }

      showValidation(`✓ Executados ${response.steps_executed} passos`, true);
    }
  } catch (error) {
    showValidation(`✗ Erro: ${error.message}`, false);
  } finally {
    hideLoading();
  }
}

// Atualizar UI
function updateUI() {
  if (!currentMachine) return;

  // Atualizar status
  elements.currentState.textContent = currentMachine.current_state || '-';
  elements.headPosition.textContent = currentMachine.head;

  const currentSymbol = currentMachine.tape[currentMachine.head.toString()] || currentMachine.blank;
  elements.currentSymbol.textContent = currentSymbol === ' ' ? '␣' : currentSymbol;

  // Atualizar badge de resultado
  updateResultBadge();

  // Renderizar fita
  renderTape();
}

function updateResultBadge() {
  const result = currentMachine.result;
  let text = 'EXECUTANDO';
  let className = 'status-badge running';

  if (!currentMachine.halted) {
    text = 'EXECUTANDO';
    className = 'status-badge running';
  } else if (result === 'ACCEPT') {
    text = 'ACEITO ✓';
    className = 'status-badge accept';
  } else if (result === 'REJECT') {
    text = 'REJEITADO ✗';
    className = 'status-badge reject';
  } else if (result === 'NO_TRANSITION') {
    text = 'SEM TRANSIÇÃO';
    className = 'status-badge error';
  } else if (result === 'MAX_STEPS') {
    text = 'LIMITE DE PASSOS';
    className = 'status-badge error';
  }

  elements.resultBadge.textContent = text;
  elements.resultBadge.className = className;
}

function renderTape() {
  const span = 15; // Células de cada lado
  const head = currentMachine.head;
  const blank = currentMachine.blank;

  const cells = [];
  for (let i = head - span; i <= head + span; i++) {
    const symbol = currentMachine.tape[i.toString()] || blank;
    const isHead = i === head;
    cells.push({ position: i, symbol, isHead });
  }

  const tapeHTML = `
        <div class="tape">
            ${cells.map(cell => `
                <div class="tape-cell ${cell.isHead ? 'active' : ''}" title="Posição ${cell.position}">
                    ${cell.symbol === ' ' ? '␣' : (cell.symbol || blank)}
                </div>
            `).join('')}
        </div>
    `;

  elements.tapeContainer.innerHTML = tapeHTML;
}

function updateTransitionsTable(spec) {
  const lines = spec.split('\n');
  const transitions = [];
  let inTransitions = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed === 'transitions:') {
      inTransitions = true;
      continue;
    }
    if (inTransitions && trimmed && !trimmed.startsWith('#')) {
      transitions.push(trimmed);
    }
  }

  if (transitions.length === 0) {
    elements.transitionsTable.innerHTML = '<p class="text-muted">Nenhuma transição definida</p>';
    return;
  }

  const transitionsHTML = transitions.map(trans => {
    // Parse: (estado, símbolo) -> (novo_estado, escrever, movimento)
    const formatted = trans
      .replace(/,/g, ' , ')
      .replace(/->/g, ' → ')
      .replace(/\s+/g, ' ');

    return `<div class="transition-item">${formatted}</div>`;
  }).join('');

  elements.transitionsTable.innerHTML = transitionsHTML;
}

function enableControls() {
  elements.stepBtn.disabled = false;
  elements.run10Btn.disabled = false;
  elements.runAllBtn.disabled = false;
}

function disableControls() {
  elements.stepBtn.disabled = true;
  elements.run10Btn.disabled = true;
  elements.runAllBtn.disabled = true;
}

// Event Listeners
elements.examplesSelect.addEventListener('change', (e) => {
  const exampleName = e.target.value;
  if (exampleName && examples[exampleName]) {
    elements.specEditor.value = examples[exampleName];
    updateTransitionsTable(examples[exampleName]);

    // Sugerir entrada baseada no exemplo
    if (exampleName.includes('0^n1^n')) {
      elements.inputField.value = '0011';
    } else if (exampleName.includes('Paridade')) {
      elements.inputField.value = '1011';
    } else if (exampleName.includes('0*1*')) {
      elements.inputField.value = '00011';
    } else if (exampleName.includes('vazia')) {
      elements.inputField.value = '';
    } else if (exampleName.includes('Duplicador')) {
      elements.inputField.value = '01';
    } else {
      elements.inputField.value = '0101';
    }
  }
});

elements.validateBtn.addEventListener('click', validateSpec);
elements.resetBtn.addEventListener('click', resetMachine);
elements.stepBtn.addEventListener('click', step);
elements.run10Btn.addEventListener('click', () => runSteps(10));
elements.runAllBtn.addEventListener('click', () => runSteps(-1));

// Atalhos de teclado
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + Enter para validar
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && document.activeElement === elements.specEditor) {
    e.preventDefault();
    validateSpec();
  }

  // Enter no campo de entrada para resetar
  if (e.key === 'Enter' && document.activeElement === elements.inputField) {
    e.preventDefault();
    resetMachine();
  }

  // Espaço para executar um passo (quando não está em input)
  if (e.key === ' ' && document.activeElement === document.body && currentMachine && !currentMachine.halted) {
    e.preventDefault();
    step();
  }
});

// Inicialização
async function init() {
  showLoading();
  try {
    await loadExamples();

    // Carregar exemplo padrão se disponível
    const defaultExample = Object.keys(examples)[0];
    if (defaultExample) {
      elements.examplesSelect.value = defaultExample;
      elements.specEditor.value = examples[defaultExample];
      elements.inputField.value = '0011';
      updateTransitionsTable(examples[defaultExample]);
    }
  } catch (error) {
    console.error('Erro na inicialização:', error);
    showValidation('Erro ao carregar exemplos', false);
  } finally {
    hideLoading();
  }

  // Adicionar dica visual inicial
  elements.resultBadge.textContent = 'AGUARDANDO';
  elements.resultBadge.className = 'status-badge waiting';
}

// Iniciar aplicação quando DOM estiver pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
