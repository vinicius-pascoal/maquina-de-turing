import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, Optional
import json

# ===============================
# Máquina de Turing — Núcleo
# ===============================
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
        # Halt if in accept/reject sets
        if self.current_state in self.accept_states:
            self.halted, self.result = True, 'ACCEPT'
            return
        if self.current_state in self.reject_states:
            self.halted, self.result = True, 'REJECT'
            return

        sym = self.read()
        key = (self.current_state, sym)
        if key not in self.transitions:
            # No transition defined
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

    def tape_to_string(self, left: int, right: int) -> str:
        return ''.join(self.tape.get(i, self.blank) for i in range(left, right + 1))


# ===============================
# Parser de Especificação (DSL simples)
# ===============================
SPEC_TEMPLATE = """
# Linguagem de especificação (DSL) — exemplo abaixo
# Linhas iniciadas com # são comentários.
# Campos obrigatórios: states, blank, start, accept, reject, transitions
# Símbolo em branco pode ser '_' ou outro caractere único.

states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject

# Formato de transição: estado_atual,simbolo_lido -> novo_estado,simbolo_escrito,Mov
# Mov ∈ {L, R, N}
transitions:
q0,0 -> q0,0,R
q0,1 -> q0,1,R
q0,_ -> qaccept,_,N
""".strip()

EXAMPLES = {
    "Aceita qualquer sequência binária (para no accept)": SPEC_TEMPLATE,
    "Incremento unário (adiciona um 1 ao final)": """
states: q0,qscan,qwrite,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
# Varre até encontrar o branco no final
q0,1 -> q0,1,R
q0,_ -> qwrite,_,L
# Escreve um 1 no fim
qwrite,_ -> qaccept,1,N
""".strip(),
    "Reconhece cadeia vazia apenas": """
states: q0,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,_ -> qaccept,_,N
q0,0 -> qreject,0,N
q0,1 -> qreject,1,N
""".strip(),
}


def parse_spec(spec_text: str) -> Tuple[TuringMachine, Optional[str]]:
    """Parsa a DSL e retorna (tm, error)."""
    try:
        # Remove comentários e linhas vazias
        lines = []
        for raw in spec_text.splitlines():
            s = raw.strip()
            if not s or s.startswith('#'):
                continue
            lines.append(s)
        text = '\n'.join(lines)

        # Separar header e bloco transitions
        if 'transitions:' not in text:
            return None, "Especificação precisa da seção 'transitions:'"
        head, body = text.split('transitions:', 1)
        header = {}
        for line in head.splitlines():
            if ':' in line:
                k, v = [x.strip() for x in line.split(':', 1)]
                header[k.lower()] = v

        required = ['states', 'blank', 'start', 'accept', 'reject']
        for r in required:
            if r not in header:
                return None, f"Campo obrigatório ausente: {r}"

        states = set([s.strip()
                     for s in header['states'].split(',') if s.strip()])
        blank = header['blank']
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


# ===============================
# UI — Streamlit
# ===============================
st.set_page_config(page_title="Máquina de Turing — Simulador",
                   page_icon="💾", layout="wide")

if 'tm' not in st.session_state:
    st.session_state.tm = None
if 'loaded_spec' not in st.session_state:
    st.session_state.loaded_spec = EXAMPLES[
        "Aceita qualquer sequência binária (para no accept)"]
if 'input_string' not in st.session_state:
    st.session_state.input_string = "1011"

st.title("💾 Simulador de Máquina de Turing")
st.caption("Python + Streamlit — defina sua MT, rode passo a passo ou até parar.")

with st.sidebar:
    st.header("⚙️ Especificação")
    preset = st.selectbox("Exemplos", list(EXAMPLES.keys()))
    if st.button("Carregar exemplo"):
        st.session_state.loaded_spec = EXAMPLES[preset]

    spec = st.text_area(
        "DSL da Máquina", value=st.session_state.loaded_spec, height=300)

    st.divider()
    st.subheader("Entrada da fita")
    st.session_state.input_string = st.text_input(
        "Conteúdo inicial da fita", value=st.session_state.input_string)
    max_steps = st.number_input("Limite de passos para 'Rodar até parar'",
                                min_value=1, max_value=100000, value=2000, step=100)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Inicializar/Resetar"):
            tm, err = parse_spec(spec)
            if err:
                st.error(err)
            else:
                tm.reset(st.session_state.input_string)
                st.session_state.tm = tm
                st.success("Máquina pronta!")
    with col_b:
        if st.button("Exportar config (JSON)"):
            tm, err = parse_spec(spec)
            if err:
                st.error(err)
            else:
                data = {
                    'states': sorted(list(tm.states)),
                    'blank': tm.blank,
                    'start_state': tm.start_state,
                    'accept_states': sorted(list(tm.accept_states)),
                    'reject_states': sorted(list(tm.reject_states)),
                    'transitions': {f"{k[0]},{k[1]}": v for k, v in tm.transitions.items()},
                }
                st.download_button("Baixar JSON", data=json.dumps(
                    data, ensure_ascii=False, indent=2), file_name="turing_machine.json")


# Área principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualização da fita")
    tm: Optional[TuringMachine] = st.session_state.tm
    if tm is None:
        st.info(
            "Use a barra lateral para carregar um exemplo e clicar em **Inicializar/Resetar**.")
    else:
        # Renderizar janela da fita em HTML
        window = 25
        left = tm.head - window
        right = tm.head + window
        cells = []
        for i in range(left, right + 1):
            sym = tm.tape.get(i, tm.blank)
            cls = "cell"
            if i == tm.head:
                cls += " head"
            cells.append((i, sym, cls))

        styles = f"""
        <style>
        .tape {{ display: grid; grid-template-columns: repeat({(right-left+1)}, 40px); gap: 2px; }}
        .cell {{ border: 1px solid #999; padding: 8px; text-align: center; font-family: monospace; border-radius: 6px; }}
        .head {{ background: #f0f7ff; border-color: #1f6feb; box-shadow: 0 0 0 2px rgba(31,111,235,0.25) inset; }}
        .legend {{ font-size: 0.9rem; color: #6b7280; margin-top: 8px; }}
        .pill {{ display:inline-block; padding: 2px 8px; border-radius: 9999px; background:#eef2ff; border:1px solid #c7d2fe; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
        </style>
        """
        html = [styles, '<div class="tape">']
        for _, sym, cls in cells:
            html.append(f'<div class="{cls}">{sym}</div>')
        html.append('</div>')
        st.markdown('\n'.join(html), unsafe_allow_html=True)

        # Estado atual e status
        st.markdown(
            f"Estado: <span class='pill'>{tm.current_state}</span> &nbsp; | &nbsp; Cabeça: <span class='pill'>{tm.head}</span> &nbsp; | &nbsp; Resultado: <span class='pill'>{tm.result or '-'} </span>",
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("◀️ Passo (1)"):
                tm.step()
                st.session_state.tm = tm
        with c2:
            n = st.number_input("Passos (run)", min_value=1,
                                max_value=100000, value=50)
            if st.button("▶️ Rodar N passos"):
                tm.run(n)
                st.session_state.tm = tm
        with c3:
            if st.button("⏭️ Rodar até parar"):
                tm.run(int(max_steps))
                st.session_state.tm = tm
        with c4:
            if st.button("🔁 Reset (mesma entrada)"):
                tm.reset(st.session_state.input_string)
                st.session_state.tm = tm

with col2:
    st.subheader("Transições ativas")
    if st.session_state.tm is None:
        st.caption("Inicialize a máquina para ver as regras relevantes.")
    else:
        tm: TuringMachine = st.session_state.tm
        sym = tm.read()
        key = (tm.current_state, sym)
        st.write("**Lendo na cabeça:**", f"`{sym}`")
        if key in tm.transitions:
            ns, ws, mv = tm.transitions[key]
            st.success(f"δ({tm.current_state}, {sym}) = ({ns}, {ws}, {mv})")
        else:
            st.error("Nenhuma transição definida para o par estado/símbolo atual.")

    st.divider()
    st.subheader("Ajuda rápida")
    st.markdown(
        """
        **Como usar**
        1. Escolha um exemplo na barra lateral (ou edite a DSL).
        2. Clique em **Inicializar/Resetar**.
        3. Use os botões **Passo**, **Rodar N passos** ou **Rodar até parar**.

        **DSL**
        - `states: q0,q1,qaccept,qreject`
        - `blank: _`  (símbolo em branco)
        - `start: q0`
        - `accept: qaccept` (pode ser lista separada por vírgula)
        - `reject: qreject` (pode ser lista separada por vírgula)
        - `transitions:` seguido de linhas no formato `estado,leitura -> novo,escrita,Mov` onde `Mov` ∈ {L,R,N}

        **Exemplo**
        ```
        states: q0,q1,qaccept,qreject
        blank: _
        start: q0
        accept: qaccept
        reject: qreject
        transitions:
        q0,0 -> q0,0,R
        q0,1 -> q0,1,R
        q0,_ -> qaccept,_,N
        ```
        """
    )

st.caption("Feito com ❤️ em Streamlit. Dica: salve este arquivo como `app.py` e rode `streamlit run app.py`.")
