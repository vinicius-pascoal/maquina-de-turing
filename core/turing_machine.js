class TuringMachine {
  constructor({
    states,
    inputSymbols,
    tapeSymbols,
    blank,
    transitions,
    startState,
    acceptStates,
    rejectStates,
    tape = {},
    head = 0,
    currentState = null,
    halted = false,
    result = null
  }) {
    this.states = new Set(states);
    this.inputSymbols = new Set(inputSymbols);
    this.tapeSymbols = new Set(tapeSymbols);
    this.blank = blank;
    this.transitions = transitions;
    this.startState = startState;
    this.acceptStates = new Set(acceptStates);
    this.rejectStates = new Set(rejectStates);
    this.tape = { ...tape };
    this.head = head;
    this.currentState = currentState;
    this.halted = halted;
    this.result = result;
  }

  reset(inputString) {
    this.tape = {};
    for (let i = 0; i < inputString.length; i++) {
      this.tape[i] = inputString[i];
    }
    this.head = 0;
    this.currentState = this.startState;
    this.halted = false;
    this.result = null;
  }

  read() {
    return this.tape[this.head] || this.blank;
  }

  write(symbol) {
    if (symbol === this.blank) {
      delete this.tape[this.head];
    } else {
      this.tape[this.head] = symbol;
    }
  }

  step() {
    if (this.halted) return;

    if (this.acceptStates.has(this.currentState)) {
      this.halted = true;
      this.result = 'ACCEPT';
      return;
    }

    if (this.rejectStates.has(this.currentState)) {
      this.halted = true;
      this.result = 'REJECT';
      return;
    }

    const sym = this.read();
    const key = `${this.currentState},${sym}`;

    if (!this.transitions[key]) {
      this.halted = true;
      this.result = 'NO_TRANSITION';
      return;
    }

    const [newState, writeSym, move] = this.transitions[key];
    this.write(writeSym);

    if (move === 'L') {
      this.head -= 1;
    } else if (move === 'R') {
      this.head += 1;
    } else if (move === 'N') {
      // Não move
    } else {
      throw new Error(`Movimento inválido: ${move}`);
    }

    this.currentState = newState;
  }

  run(maxSteps = 1000) {
    let steps = 0;
    while (!this.halted && steps < maxSteps) {
      this.step();
      steps++;
    }
    if (!this.halted && steps >= maxSteps) {
      this.halted = true;
      this.result = 'MAX_STEPS';
    }
    return steps;
  }

  windowCells(span = 25) {
    const left = this.head - span;
    const right = this.head + span;
    const cells = [];
    for (let i = left; i <= right; i++) {
      cells.push([i, this.tape[i] || this.blank, i === this.head]);
    }
    return cells;
  }

  toDict() {
    return {
      states: Array.from(this.states),
      input_symbols: Array.from(this.inputSymbols),
      tape_symbols: Array.from(this.tapeSymbols),
      blank: this.blank,
      transitions: this.transitions,
      start_state: this.startState,
      accept_states: Array.from(this.acceptStates),
      reject_states: Array.from(this.rejectStates),
      tape: this.tape,
      head: this.head,
      current_state: this.currentState,
      halted: this.halted,
      result: this.result
    };
  }

  static fromDict(data) {
    return new TuringMachine({
      states: data.states,
      inputSymbols: data.input_symbols,
      tapeSymbols: data.tape_symbols,
      blank: data.blank,
      transitions: data.transitions,
      startState: data.start_state,
      acceptStates: data.accept_states,
      rejectStates: data.reject_states,
      tape: typeof data.tape === 'object' ? data.tape : {},
      head: data.head,
      currentState: data.current_state,
      halted: data.halted,
      result: data.result
    });
  }
}

function parseSpec(specText) {
  try {
    const lines = specText
      .split('\n')
      .map(line => line.trim())
      .filter(line => line && !line.startsWith('#'));

    const text = lines.join('\n');

    if (!text.includes('transitions:')) {
      return { tm: null, error: "Especificação precisa da seção 'transitions:'" };
    }

    const [head, body] = text.split('transitions:');

    const header = {};
    for (const line of head.split('\n')) {
      if (line.includes(':')) {
        const [k, v] = line.split(':', 2).map(s => s.trim());
        let vClean = v.trim();
        if ((vClean.startsWith("'") && vClean.endsWith("'")) ||
          (vClean.startsWith('"') && vClean.endsWith('"'))) {
          vClean = vClean.slice(1, -1);
        }
        header[k.toLowerCase()] = vClean;
      }
    }

    const required = ['states', 'blank', 'start', 'accept', 'reject'];
    for (const r of required) {
      if (!header[r]) {
        return { tm: null, error: `Campo obrigatório ausente: ${r}` };
      }
    }

    const states = new Set(header.states.split(',').map(s => s.trim()).filter(s => s));
    let blank = header.blank;
    if (blank === '') blank = '_';
    if (blank.length !== 1) {
      return { tm: null, error: "O campo 'blank' deve conter exatamente 1 caractere (ex.: _ ou espaço)." };
    }

    const start = header.start;
    const accept = new Set(header.accept.split(',').map(s => s.trim()).filter(s => s));
    const reject = new Set(header.reject.split(',').map(s => s.trim()).filter(s => s));

    const transitions = {};
    const tapeSymbols = new Set([blank]);
    const inputSymbols = new Set();

    for (const line of body.split('\n')) {
      if (!line.trim()) continue;
      if (!line.includes('->') || !line.includes(',')) {
        return { tm: null, error: `Linha de transição inválida: ${line}` };
      }

      const [left, right] = line.split('->').map(s => s.trim());
      const [sState, sRead] = left.split(',', 2).map(s => s.trim());
      const parts = right.split(',').map(s => s.trim());

      if (parts.length !== 3) {
        return { tm: null, error: `Formato de transição inválido: ${line}` };
      }

      const [nState, sWrite, sMove] = parts;

      if (!['L', 'R', 'N'].includes(sMove)) {
        return { tm: null, error: `Movimento inválido em: ${line}` };
      }

      transitions[`${sState},${sRead}`] = [nState, sWrite, sMove];
      tapeSymbols.add(sRead);
      tapeSymbols.add(sWrite);
      if (sRead !== blank) {
        inputSymbols.add(sRead);
      }
    }

    const tm = new TuringMachine({
      states,
      inputSymbols: inputSymbols.size > 0 ? inputSymbols : new Set(['0', '1']),
      tapeSymbols,
      blank,
      transitions,
      startState: start,
      acceptStates: accept,
      rejectStates: reject
    });

    return { tm, error: null };
  } catch (e) {
    return { tm: null, error: `Erro ao parsear especificação: ${e.message}` };
  }
}

export { TuringMachine, parseSpec };
