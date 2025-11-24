from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, Optional

Move = str  # 'L' | 'R' | 'N'
Transition = Tuple[str, str, Move]


@dataclass
class TuringMachine:
    states: Set[str]
    input_symbols: Set[str]
    tape_symbols: Set[str]
    blank: str
    transitions: Dict[Tuple[str, str], Transition]
    start_state: str
    accept_states: Set[str]
    reject_states: Set[str]
    tape: Dict[int, str] = field(default_factory=dict)
    head: int = 0
    current_state: Optional[str] = None
    halted: bool = False
    # 'ACCEPT' | 'REJECT' | 'NO_TRANSITION' | 'MAX_STEPS'
    result: Optional[str] = None

    def reset(self, input_string: str):
        self.tape = {}
        for i, ch in enumerate(input_string):
            self.tape[i] = ch
        self.head = 0
        self.current_state = self.start_state
        self.halted = False
        self.result = None

    def read(self) -> str:
        return self.tape.get(self.head, self.blank)

    def write(self, symbol: str):
        if symbol == self.blank:
            if self.head in self.tape:
                del self.tape[self.head]
        else:
            self.tape[self.head] = symbol

    def step(self) -> None:
        if self.halted:
            return
        if self.current_state in self.accept_states:
            self.halted, self.result = True, 'ACCEPT'
            return
        if self.current_state in self.reject_states:
            self.halted, self.result = True, 'REJECT'
            return

        sym = self.read()
        key = (self.current_state, sym)
        if key not in self.transitions:
            self.halted = True
            self.result = 'NO_TRANSITION'
            return
        new_state, write_sym, move = self.transitions[key]
        self.write(write_sym)
        if move == 'L':
            self.head -= 1
        elif move == 'R':
            self.head += 1
        elif move == 'N':
            pass
        else:
            raise ValueError(f"Movimento inválido: {move}")
        self.current_state = new_state

    def run(self, max_steps: int = 1000):
        steps = 0
        while not self.halted and steps < max_steps:
            self.step()
            steps += 1
        if not self.halted and steps >= max_steps:
            self.halted = True
            self.result = 'MAX_STEPS'
        return steps

    def window_cells(self, span: int = 25):
        left = self.head - span
        right = self.head + span
        return [(i, self.tape.get(i, self.blank), (i == self.head)) for i in range(left, right + 1)]

    def to_dict(self):
        """Converte para dicionário serializável"""
        return {
            'states': list(self.states),
            'input_symbols': list(self.input_symbols),
            'tape_symbols': list(self.tape_symbols),
            'blank': self.blank,
            'transitions': {f"{k[0]},{k[1]}": list(v) for k, v in self.transitions.items()},
            'start_state': self.start_state,
            'accept_states': list(self.accept_states),
            'reject_states': list(self.reject_states),
            'tape': {str(k): v for k, v in self.tape.items()},
            'head': self.head,
            'current_state': self.current_state,
            'halted': self.halted,
            'result': self.result
        }

    @classmethod
    def from_dict(cls, data):
        """Cria instância a partir de dicionário"""
        transitions = {}
        for k, v in data['transitions'].items():
            state, sym = k.split(',', 1)
            transitions[(state, sym)] = tuple(v)

        return cls(
            states=set(data['states']),
            input_symbols=set(data['input_symbols']),
            tape_symbols=set(data['tape_symbols']),
            blank=data['blank'],
            transitions=transitions,
            start_state=data['start_state'],
            accept_states=set(data['accept_states']),
            reject_states=set(data['reject_states']),
            tape={int(k): v for k, v in data['tape'].items()},
            head=data['head'],
            current_state=data['current_state'],
            halted=data['halted'],
            result=data['result']
        )


def parse_spec(spec_text: str):
    """Parser da DSL para Máquina de Turing"""
    try:
        lines = []
        for raw in spec_text.splitlines():
            s = raw.strip()
            if not s or s.startswith('#'):
                continue
            lines.append(s)
        text = '\n'.join(lines)

        if 'transitions:' not in text:
            return None, "Especificação precisa da seção 'transitions:'"
        head, body = text.split('transitions:', 1)

        header: Dict[str, str] = {}
        for line in head.splitlines():
            if ':' in line:
                k, v = [x.strip() for x in line.split(':', 1)]
                v_clean = v.strip()
                if (v_clean.startswith("'") and v_clean.endswith("'")) or (v_clean.startswith('"') and v_clean.endswith('"')):
                    v_clean = v_clean[1:-1]
                header[k.lower()] = v_clean

        required = ['states', 'blank', 'start', 'accept', 'reject']
        for r in required:
            if r not in header:
                return None, f"Campo obrigatório ausente: {r}"

        states = set([s.strip()
                     for s in header['states'].split(',') if s.strip()])
        blank = header['blank']
        if blank == "":
            blank = "_"
        if len(blank) != 1:
            return None, "O campo 'blank' deve conter exatamente 1 caractere (ex.: _ ou espaço)."

        start = header['start']
        accept = set([s.strip()
                     for s in header['accept'].split(',') if s.strip()])
        reject = set([s.strip()
                     for s in header['reject'].split(',') if s.strip()])

        transitions: Dict[Tuple[str, str], Transition] = {}
        tape_symbols: Set[str] = set([blank])
        input_symbols: Set[str] = set()

        for line in body.splitlines():
            if not line:
                continue
            if '->' not in line or ',' not in line:
                return None, f"Linha de transição inválida: {line}"
            left, right = [x.strip() for x in line.split('->', 1)]
            s_state, s_read = [x.strip() for x in left.split(',', 1)]
            n_state, s_write, s_move = [x.strip() for x in right.split(',', 2)]
            if s_move not in ('L', 'R', 'N'):
                return None, f"Movimento inválido em: {line}"
            transitions[(s_state, s_read)] = (n_state, s_write, s_move)
            tape_symbols.add(s_read)
            tape_symbols.add(s_write)
            if s_read != blank:
                input_symbols.add(s_read)

        tm = TuringMachine(
            states=states,
            input_symbols=input_symbols or set(['0', '1']),
            tape_symbols=tape_symbols,
            blank=blank,
            transitions=transitions,
            start_state=start,
            accept_states=accept,
            reject_states=reject,
        )
        return tm, None
    except Exception as e:
        return None, f"Erro ao parsear especificação: {e}"
