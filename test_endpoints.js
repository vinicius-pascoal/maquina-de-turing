// Script de teste para verificar todos os endpoints da API

const BASE_URL = 'http://localhost:3000/api';

async function testExamples() {
  console.log('🧪 Testando /api/examples...');
  try {
    const response = await fetch(`${BASE_URL}/examples`);
    const data = await response.json();
    console.log('✅ /api/examples:', data.success ? 'OK' : 'FALHOU');
    console.log(`   Exemplos encontrados: ${Object.keys(data.examples || {}).length}`);
    return data.success;
  } catch (e) {
    console.log('❌ /api/examples: ERRO -', e.message);
    return false;
  }
}

async function testValidate() {
  console.log('\n🧪 Testando /api/validate...');
  try {
    const spec = `states: q0,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,_ -> qaccept,_,N`;

    const response = await fetch(`${BASE_URL}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ spec })
    });
    const data = await response.json();
    console.log('✅ /api/validate:', data.success ? 'OK' : 'FALHOU');
    if (data.success) {
      console.log(`   Estados: ${data.states?.length}, Transições: ${data.transitions_count}`);
    } else {
      console.log(`   Erro: ${data.error}`);
    }
    return data.success;
  } catch (e) {
    console.log('❌ /api/validate: ERRO -', e.message);
    return false;
  }
}

async function testReset() {
  console.log('\n🧪 Testando /api/reset...');
  try {
    const spec = `states: q0,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,_ -> qaccept,_,N`;

    const response = await fetch(`${BASE_URL}/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ spec, input: '000' })
    });
    const data = await response.json();
    console.log('✅ /api/reset:', data.success ? 'OK' : 'FALHOU');
    if (data.success) {
      console.log(`   Estado inicial: ${data.machine?.current_state}, Head: ${data.machine?.head}`);
    } else {
      console.log(`   Erro: ${data.error}`);
    }
    return data.success;
  } catch (e) {
    console.log('❌ /api/reset: ERRO -', e.message);
    return false;
  }
}

async function testStep() {
  console.log('\n🧪 Testando /api/step...');
  try {
    // Primeiro, cria uma máquina
    const spec = `states: q0,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,_ -> qaccept,_,N`;

    const resetResponse = await fetch(`${BASE_URL}/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ spec, input: '000' })
    });
    const resetData = await resetResponse.json();

    if (!resetData.success) {
      console.log('❌ /api/step: Falha ao criar máquina');
      return false;
    }

    // Agora testa step
    const stepResponse = await fetch(`${BASE_URL}/step`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ machine: resetData.machine })
    });
    const stepData = await stepResponse.json();
    console.log('✅ /api/step:', stepData.success ? 'OK' : 'FALHOU');
    if (stepData.success) {
      console.log(`   Head moveu para: ${stepData.machine?.head}, Estado: ${stepData.machine?.current_state}`);
    } else {
      console.log(`   Erro: ${stepData.error}`);
    }
    return stepData.success;
  } catch (e) {
    console.log('❌ /api/step: ERRO -', e.message);
    return false;
  }
}

async function testRun() {
  console.log('\n🧪 Testando /api/run...');
  try {
    // Primeiro, cria uma máquina
    const spec = `states: q0,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,_ -> qaccept,_,N`;

    const resetResponse = await fetch(`${BASE_URL}/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ spec, input: '000' })
    });
    const resetData = await resetResponse.json();

    if (!resetData.success) {
      console.log('❌ /api/run: Falha ao criar máquina');
      return false;
    }

    // Agora testa run com 10 passos
    const runResponse = await fetch(`${BASE_URL}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ machine: resetData.machine, steps: 10 })
    });
    const runData = await runResponse.json();
    console.log('✅ /api/run:', runData.success ? 'OK' : 'FALHOU');
    if (runData.success) {
      console.log(`   Passos executados: ${runData.steps_executed}, Resultado: ${runData.machine?.result}`);
    } else {
      console.log(`   Erro: ${runData.error}`);
    }
    return runData.success;
  } catch (e) {
    console.log('❌ /api/run: ERRO -', e.message);
    return false;
  }
}

async function runAllTests() {
  console.log('🚀 Iniciando testes dos endpoints...\n');

  const results = {
    examples: await testExamples(),
    validate: await testValidate(),
    reset: await testReset(),
    step: await testStep(),
    run: await testRun()
  };

  console.log('\n📊 Resumo dos Testes:');
  console.log('====================');
  for (const [name, passed] of Object.entries(results)) {
    console.log(`${passed ? '✅' : '❌'} ${name}`);
  }

  const totalPassed = Object.values(results).filter(r => r).length;
  const total = Object.keys(results).length;
  console.log(`\n${totalPassed}/${total} testes passaram`);
}

// Executar os testes
runAllTests();
