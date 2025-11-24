from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, Optional
import json
import time
import gradio as gr

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


# ===============================
# DSL base + Exemplos
# ===============================
SPEC_TEMPLATE = """
# Linguagem de especificação (DSL)
# Linhas iniciadas com # são comentários.
# Campos: states, blank, start, accept, reject, transitions
# Movimento: L, R, N

states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject

transitions:
q0,0 -> q0,0,R
q0,1 -> q0,1,R
q0,_ -> qaccept,_,N
""".strip()

EXAMPLES = {
    "Aceita qualquer sequência binária (para no accept)": SPEC_TEMPLATE,

    # 0^n1^n
    "0^n1^n (mesma quantidade de 0 e 1)": """
states: q0,q1,q2,qcheck,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,X -> q0,X,R
q0,Y -> q0,Y,R
q0,0 -> q1,X,R
q0,1 -> qreject,1,N
q0,_ -> qcheck,_,L

q1,X -> q1,X,R
q1,Y -> q1,Y,R
q1,0 -> qreject,0,N
q1,1 -> q2,Y,L
q1,_ -> qreject,_,N

q2,X -> q2,X,L
q2,Y -> q2,Y,L
q2,0 -> q2,0,L
q2,1 -> q2,1,L
q2,_ -> q0,_,R

qcheck,X -> qcheck,X,R
qcheck,Y -> qcheck,Y,R
qcheck,0 -> qreject,0,N
qcheck,1 -> qreject,1,N
qcheck,_ -> qaccept,_,N
""".strip(),

    # Paridade de 1's
    "Paridade de 1s (aceita se quantidade for par)": """
states: qeven,qodd,qaccept,qreject
blank: _
start: qeven
accept: qaccept
reject: qreject
transitions:
qeven,0 -> qeven,0,R
qeven,1 -> qodd,1,R
qeven,_ -> qaccept,_,N

qodd,0 -> qodd,0,R
qodd,1 -> qeven,1,R
qodd,_ -> qreject,_,N
""".strip(),

    # Soma unária 1^m#1^n -> 1^(m+n)
    "Soma unária 1^m#1^n → 1^(m+n)": """
states: q0,q1,q2,q2b,q3,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q0,1,R
q0,* -> q0,*,R
q0,# -> q1,*,R
q0,_ -> qreject,_,N

q1,1 -> q2,_,L
q1,* -> q1,*,R
q1,_ -> q3,_,L

q2,1 -> q2,1,L
q2,_ -> q2,_,L
q2,* -> q2b,1,R

q2b,_ -> q1,*,R
q2b,1 -> qreject,1,N

q3,1 -> q3,1,L
q3,_ -> q3,_,L
q3,* -> qaccept,_,N
""".strip(),

    # 0*1*
    "Linguagem 0*1* (todos 0 antes dos 1)": """
states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q0,0,R
q0,1 -> q1,1,R
q0,_ -> qaccept,_,N

q1,1 -> q1,1,R
q1,0 -> qreject,0,N
q1,_ -> qaccept,_,N
""".strip(),

    # Incremento unário (exemplo simples)
    "Incremento unário (adiciona um 1 ao final)": """
states: q0,qwrite,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q0,1,R
q0,_ -> qwrite,_,L
qwrite,_ -> qaccept,1,N
""".strip(),

    # Cadeia vazia
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

# ===============================
# Parser da DSL
# ===============================


def parse_spec(spec_text: str):
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

# ===============================
# Helpers de UI com design melhorado
# ===============================


def render_tape_html(tm: Optional[TuringMachine], span: int = 25, cell_px: int = 36, show_invis: bool = False) -> str:
    if tm is None:
        return """
        <div style='text-align:center; padding:60px 20px; background:linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius:16px; color:white;'>
            <div style='font-size:48px; margin-bottom:16px; font-weight:bold;'>MT</div>
            <p style='font-size:18px; margin:0; opacity:0.95;'>Inicialize a máquina para visualizar a fita</p>
        </div>
        """

    cells = tm.window_cells(span)
    cols = len(cells)

    def display(sym: str) -> str:
        if show_invis and (sym == "" or sym == " " or sym == "\t" or sym == "\n" or sym == "\r"):
            return "□"
        return sym

    # Determina a cor do estado baseado no resultado
    state_color = "#6366f1"  # azul padrão
    state_bg = "#eef2ff"
    if tm.result == 'ACCEPT':
        state_color = "#10b981"
        state_bg = "#d1fae5"
    elif tm.result == 'REJECT':
        state_color = "#ef4444"
        state_bg = "#fee2e2"
    elif tm.result in ['NO_TRANSITION', 'MAX_STEPS']:
        state_color = "#f59e0b"
        state_bg = "#fef3c7"

    styles = f"""
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes slideIn {{
        from {{ transform: translateX(-20px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    .tape-container {{
        background: linear-gradient(135deg, #131b23 0%, #1e3151 100%);
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        animation: fadeIn 0.6s ease-out;
    }}

    .tape {{
        display: grid;
        grid-template-columns: repeat({cols}, {cell_px}px);
        gap: 4px;
        justify-content: center;
        overflow-x: auto;
        padding: 16px 0;
        margin: 0 auto;
        max-width: 100%;
    }}

    .tape::-webkit-scrollbar {{
        height: 8px;
    }}

    .tape::-webkit-scrollbar-track {{
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }}

    .tape::-webkit-scrollbar-thumb {{
        background: rgba(99,102,241,0.5);
        border-radius: 10px;
    }}

    .tape::-webkit-scrollbar-thumb:hover {{
        background: rgba(99,102,241,0.7);
    }}

    .cell {{
        border: 2px solid #e2e8f0;
        padding: 10px;
        text-align: center;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
        border-radius: 12px;
        background: black;
        color: #1e293b;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.2;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}

    .cell::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.5), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}

    .cell:hover::before {{
        opacity: 1;
    }}

    .head {{
        background: black;
        color: #ffffff;
        border-color: #4f46e5;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4),
                    0 0 0 3px rgba(99, 102, 241, 0.1);
        font-weight: 700;
        transform: scale(1.08);
        z-index: 10;
    }}

    .head::after {{
        content: '▼';
        position: absolute;
        top: -24px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 16px;
        color: #6366f1;
        animation: bounce 1s ease-in-out infinite;
    }}

    @keyframes bounce {{
        0%, 100% {{ transform: translateX(-50%) translateY(0); }}
        50% {{ transform: translateX(-50%) translateY(-5px); }}
    }}

    .info-panel {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 24px;
        margin-top: 28px;
        flex-wrap: wrap;
        animation: slideIn 0.8s ease-out;
    }}

    .info-card {{
        background: black;
        border-radius: 14px;
        padding: 14px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }}

    .info-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }}

    .info-label {{
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .info-value {{
        font-family: 'SF Mono', monospace;
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
        padding: 6px 14px;
        border-radius: 8px;
    }}

    .state-card {{
        background: black;
        border-color: {state_color};
    }}

    .state-card .info-value {{
        color: white;
    }}

    .position-icon {{
        font-size: 20px;
    }}

    .legend {{
        text-align: center;
        margin-top: 20px;
        padding: 16px;
        background: black;
        border-radius: 12px;
        font-size: 13px;
        color: #64748b;
        backdrop-filter: blur(10px);
    }}
    </style>
    """

    html = [styles, '<div class="tape-container">']
    html.append('<div class="tape">')

    for _, sym, is_head in cells:
        cls = "cell head" if is_head else "cell"
        shown = display(sym if sym != tm.blank else sym)
        html.append(f'<div class="{cls}">{shown}</div>')

    html.append('</div>')

    # Painel de informações melhorado
    result_display = tm.result if tm.result else "Executando"
    result_icon = {
        'ACCEPT': '&#10003;',  # Checkmark
        'REJECT': '&#10007;',  # Cross mark
        'NO_TRANSITION': '&#9888;',  # Warning sign
        'MAX_STEPS': '&#9203;',  # Stopwatch
        None: '&#9654;'  # Play symbol
    }.get(tm.result, '&#9654;')

    html.append('<div class="info-panel">')
    html.append(f'''
        <div class="info-card state-card">
            <span class="info-label">Estado Atual</span>
            <span class="info-value">{tm.current_state}</span>
        </div>
        <div class="info-card">
            <span class="position-icon">&#128205;</span>
            <span class="info-label">Posição</span>
            <span class="info-value">{tm.head}</span>
        </div>
        <div class="info-card">
            <span style="font-size:20px">{result_icon}</span>
            <span class="info-label">Status</span>
            <span class="info-value">{result_display}</span>
        </div>
    ''')
    html.append('</div>')

    html.append(
        '<div class="legend">A célula destacada indica a posição atual da cabeça de leitura/escrita</div>')
    html.append('</div>')

    return '\n'.join(html)


def next_transition(tm: Optional[TuringMachine]) -> str:
    if tm is None:
        return "—"
    sym = tm.read()
    key = (tm.current_state, sym)
    if key in tm.transitions:
        ns, ws, mv = tm.transitions[key]
        move_name = {'L': '&#8592;', 'R': '&#8594;', 'N': '&#8226;'}[mv]
        return f"&#948;({tm.current_state}, {sym}) &#8594; ({ns}, {ws}, {move_name})"
    return "Nenhuma transição definida para o par estado/símbolo atual"


def transitions_table(spec_text: str) -> str:
    tm, err = parse_spec(spec_text)
    if err:
        return f"Erro: {err}"
    rows = ["| Estado, Leitura | Novo Estado, Escrita, Movimento |", "|:---:|:---:|"]
    for (s, a) in sorted(tm.transitions.keys(), key=lambda x: (x[0], x[1])):
        ns, ws, mv = tm.transitions[(s, a)]
        move_symbol = {'L': '&#8592;', 'R': '&#8594;', 'N': '&#8226;'}[mv]
        rows.append(f"| `{s}`, `{a}` | `{ns}`, `{ws}`, {move_symbol} |")
    return "\n".join(rows)

# ===============================
# Ações da UI
# ===============================


def ui_load_example(example_key: str):
    return EXAMPLES.get(example_key, SPEC_TEMPLATE)


def ui_initialize(spec_text: str, input_string: str, span: int, cell_px: int):
    tm, err = parse_spec(spec_text)
    if err:
        return None, f"Erro: {err}", render_tape_html(None, span, cell_px, show_invis=False), "—"
    tm.reset(input_string)
    return tm, "Máquina inicializada com sucesso!", render_tape_html(tm, span, cell_px, show_invis=False), next_transition(tm)


def ui_reset_same_input(tm: Optional[TuringMachine], spec_text: str, input_string: str, span: int, cell_px: int):
    if tm is None:
        return ui_initialize(spec_text, input_string, span, cell_px)
    tm.reset(input_string)
    return tm, "Máquina reiniciada com a mesma entrada", render_tape_html(tm, span, cell_px, show_invis=False), next_transition(tm)


def ui_step(tm: Optional[TuringMachine], span: int, cell_px: int):
    if tm is None:
        return None, "Por favor, inicialize a máquina primeiro", render_tape_html(None, span, cell_px, show_invis=False), "—"
    tm.step()
    msg = "Passo executado"
    if tm.halted:
        msg = f"Execução finalizada: {tm.result}"
    return tm, msg, render_tape_html(tm, span, cell_px, show_invis=False), next_transition(tm)


def ui_run_n(tm: Optional[TuringMachine], n: int, span: int, cell_px: int):
    if tm is None:
        return None, "Por favor, inicialize a máquina primeiro", render_tape_html(None, span, cell_px, show_invis=False), "—"
    n = max(1, int(n))
    tm.run(n)
    msg = f"Executados {n} passos"
    if tm.halted:
        msg = f"Execução finalizada: {tm.result}"
    return tm, msg, render_tape_html(tm, span, cell_px, show_invis=False), next_transition(tm)


def ui_run_to_halt(tm: Optional[TuringMachine], max_steps: int, span: int, cell_px: int):
    if tm is None:
        return None, "Por favor, inicialize a máquina primeiro", render_tape_html(None, span, cell_px, show_invis=False), "—"
    steps = tm.run(int(max_steps))
    msg = f"Execução concluída em {steps} passos. Resultado: {tm.result}"
    return tm, msg, render_tape_html(tm, span, cell_px, show_invis=False), next_transition(tm)


def ui_play_stream(tm: Optional[TuringMachine], fps: float, max_steps: int, span: int, cell_px: int):
    if tm is None:
        yield None, "Por favor, inicialize a máquina primeiro", render_tape_html(None, span, cell_px, show_invis=False), "—"
    else:
        delay = 1.0 / max(1.0, float(fps))
        steps = 0
        while not tm.halted and steps < int(max_steps):
            tm.step()
            steps += 1
            msg = f"Executando... Passo {steps}"
            if tm.halted:
                msg = f"Finalizado: {tm.result} (após {steps} passos)"
            yield tm, msg, render_tape_html(tm, span, cell_px, show_invis=False), next_transition(tm)
            time.sleep(delay)


def ui_export_json(tm: Optional[TuringMachine]):
    if tm is None:
        return gr.update(value="Por favor, inicialize a máquina primeiro"), ""
    data = {
        'states': sorted(list(tm.states)),
        'blank': tm.blank,
        'start_state': tm.start_state,
        'accept_states': sorted(list(tm.accept_states)),
        'reject_states': sorted(list(tm.reject_states)),
        'transitions': {f"{k[0]},{k[1]}": v for k, v in tm.transitions.items()},
    }
    return gr.update(value="Configuração exportada com sucesso"), json.dumps(data, ensure_ascii=False, indent=2)


# ===============================
# Interface (Gradio) - Design melhorado
# ===============================
with gr.Blocks(title="Simulador de Máquina de Turing") as demo:
    gr.Markdown("""
    # Simulador de Máquina de Turing
    ### Visualize e controle a execução de uma Máquina de Turing com interface interativa
    """)

    with gr.Tabs() as tabs:
        with gr.TabItem("Editor", id=0):
            with gr.Row():
                with gr.Column(scale=1):
                    example_dd = gr.Dropdown(
                        choices=list(EXAMPLES.keys()),
                        value=list(EXAMPLES.keys())[0],
                        label="Exemplos Predefinidos"
                    )
                    btn_load = gr.Button(
                        "Carregar Exemplo", variant="secondary", size="sm")
                    spec_tb = gr.Textbox(
                        value=SPEC_TEMPLATE,
                        label="Especificação DSL da Máquina",
                        lines=22,
                        placeholder="Digite a especificação da máquina..."
                    )
                    preview_tbl = gr.Markdown(transitions_table(
                        SPEC_TEMPLATE), label="Transições")

                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### Guia Rápido da DSL

                    **Formato das transições:**
                    ```
                    estado, leitura -> novo_estado, escrita, movimento
                    ```

                    **Movimentos disponíveis:**
                    - `L` : Move à esquerda &#8592;
                    - `R` : Move à direita &#8594;
                    - `N` : Não move &#8226;

                    **Campos obrigatórios:**
                    - `states` : Estados da máquina
                    - `blank` : Símbolo em branco
                    - `start` : Estado inicial
                    - `accept` : Estados de aceitação
                    - `reject` : Estados de rejeição
                    - `transitions:` : Seção de transições

                    **Exemplo:**
                    ```
                    q0,0 -> q1,X,R
                    ```
                    Lê 0 no estado q0, escreve X, vai para q1 e move à direita
                    """)
                    btn_refresh_tbl = gr.Button(
                        "Atualizar Tabela de Transições", variant="secondary")

                    gr.Markdown("### Configurações")
                    input_tb = gr.Textbox(
                        value="1011",
                        label="Entrada (Cadeia Inicial na Fita)",
                        placeholder="Digite a entrada..."
                    )
                    span_slider = gr.Slider(
                        5, 40, value=25, step=1,
                        label="Janela de Visualização (&#177; células)"
                    )
                    cell_px_slider = gr.Slider(
                        24, 64, value=36, step=2,
                        label="Largura das Células (px)"
                    )

        with gr.TabItem("Execução", id=1):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Status e Controles")
                    status_out = gr.Textbox(
                        label="Mensagem de Status",
                        value="Aguardando inicialização...",
                        interactive=False
                    )
                    next_trans = gr.Textbox(
                        label="Próxima Transição &#948;(q, a)",
                        value="—",
                        interactive=False
                    )

                    gr.Markdown("#### Controles Básicos")
                    with gr.Row():
                        btn_init = gr.Button("Inicializar", variant="primary")
                        btn_reset = gr.Button("Resetar", variant="secondary")

                    gr.Markdown("#### Execução Passo a Passo")
                    with gr.Row():
                        btn_step = gr.Button(
                            "Executar 1 Passo", variant="secondary")
                    with gr.Row():
                        steps_num = gr.Number(
                            value=50, label="Número de passos", precision=0)
                        btn_run_n = gr.Button(
                            "Executar N Passos", variant="secondary")

                    gr.Markdown("#### Execução Completa")
                    with gr.Row():
                        max_steps_num = gr.Number(
                            value=2000,
                            label="Limite máximo de passos",
                            precision=0
                        )
                        btn_run_halt = gr.Button(
                            "Executar até Parar", variant="primary")

                    gr.Markdown("#### Animação em Tempo Real")
                    with gr.Row():
                        fps_num = gr.Number(
                            value=8, label="Velocidade (FPS)", precision=1)
                        play_max_steps = gr.Number(
                            value=200,
                            label="Passos máximos (animação)",
                            precision=0
                        )
                    btn_play = gr.Button(
                        "Reproduzir Animação", variant="primary")

                    gr.Markdown("#### Exportar Configuração")
                    btn_export = gr.Button(
                        "Exportar como JSON", variant="secondary")
                    export_json_status = gr.Textbox(
                        label="Status da exportação",
                        interactive=False
                    )
                    export_json_box = gr.Code(
                        label="JSON Gerado",
                        language="json",
                        lines=10
                    )

                with gr.Column(scale=2):
                    gr.Markdown("### Visualização da Fita")
                    tape_html = gr.HTML(
                        render_tape_html(None, show_invis=False))

        with gr.TabItem("Tabela de Transições", id=2):
            gr.Markdown("""
            ### Todas as Transições Definidas
            Esta tabela mostra todas as transições da máquina de Turing atual.
            """)
            trans_tbl_live = gr.Markdown(transitions_table(SPEC_TEMPLATE))

    tm_state = gr.State(value=None)

    # Editor - Eventos
    btn_load.click(
        ui_load_example,
        inputs=example_dd,
        outputs=spec_tb
    )
    btn_refresh_tbl.click(
        transitions_table,
        inputs=spec_tb,
        outputs=preview_tbl
    )

    # Execução - Eventos
    btn_init.click(
        ui_initialize,
        inputs=[spec_tb, input_tb, span_slider, cell_px_slider],
        outputs=[tm_state, status_out, tape_html, next_trans]
    )
    btn_reset.click(
        ui_reset_same_input,
        inputs=[tm_state, spec_tb, input_tb, span_slider, cell_px_slider],
        outputs=[tm_state, status_out, tape_html, next_trans]
    )
    btn_step.click(
        ui_step,
        inputs=[tm_state, span_slider, cell_px_slider],
        outputs=[tm_state, status_out, tape_html, next_trans]
    )
    btn_run_n.click(
        ui_run_n,
        inputs=[tm_state, steps_num, span_slider, cell_px_slider],
        outputs=[tm_state, status_out, tape_html, next_trans]
    )
    btn_run_halt.click(
        ui_run_to_halt,
        inputs=[tm_state, max_steps_num, span_slider, cell_px_slider],
        outputs=[tm_state, status_out, tape_html, next_trans]
    )

    # Streaming
    btn_play.click(
        ui_play_stream,
        inputs=[tm_state, fps_num, play_max_steps,
                span_slider, cell_px_slider],
        outputs=[tm_state, status_out, tape_html, next_trans]
    )

    # Export
    btn_export.click(
        ui_export_json,
        inputs=tm_state,
        outputs=[export_json_status, export_json_box]
    )

    # Atualizar tabela de transições quando mudar de aba
    spec_tb.change(
        transitions_table,
        inputs=spec_tb,
        outputs=trans_tbl_live
    )

if __name__ == "__main__":
    demo.launch(share=True)
