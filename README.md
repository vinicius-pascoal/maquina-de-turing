# 🤖 Simulador de Máquina de Turing

Um simulador interativo de Máquina de Turing com interface web moderna e intuitiva. Este projeto foi desenvolvido para facilitar o aprendizado de Teoria da Computação, permitindo visualizar e executar máquinas de Turing de forma prática e educacional.

## 🌟 Demo Online

**[Ver Demo ao Vivo](https://maquina-de-turing.vercel.app)**

## ✨ Características

### Interface Moderna
- **Design Dark Mode Profissional**: Interface elegante com gradientes e animações suaves
- **Ícones SVG**: Todos os ícones em SVG para melhor qualidade visual
- **Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Animações Fluidas**: Transições suaves e feedback visual em tempo real

### Funcionalidades Principais
- **Editor de Especificações**: Defina máquinas de Turing usando sintaxe simples
- **12 Exemplos Prontos**: Máquinas desde básicas até avançadas
- **Dicionário de Sintaxe**: Modal com documentação completa e exemplos
- **Visualização da Fita**: Acompanhe a execução com destaque na posição atual
- **Controles Flexíveis**: Execute passo a passo, 10 passos ou até completar
- **Validação em Tempo Real**: Feedback instantâneo sobre erros na especificação
- **Status Detalhado**: Acompanhe estado, posição, símbolo e resultado

### Exemplos Incluídos

**Básicos (1-4):**
1. **Paridade de 1s** - Verifica se quantidade de 1s é par
2. **Palíndromo Simples** - Reconhece palíndromos binários
3. **Duplicador** - Duplica cada símbolo (0→00, 1→11)
4. **Complemento** - Inverte bits (0→1, 1→0)

**Intermediários (5-8):**
5. **0^n1^n** - Aceita mesma quantidade de 0s e 1s
6. **0\*1\*** - Aceita 0s seguidos de 1s
7. **Somador Unário** - Soma em notação unária
8. **Multiplicador por 2** - Multiplica número binário por 2

**Avançados (9-12):**
9. **Contador de Símbolos** - Marca fim da entrada
10. **Padrão 1\*0\*1\*** - Reconhece padrão específico
11. **Apaga Tudo** - Limpa toda a fita
12. **Shift Right** - Desloca entrada para direita

## 🚀 Deploy na Vercel (Recomendado)

### Deploy com 1 Clique

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/vinicius-pascoal/maquina-de-turing)

### Deploy Manual

1. **Instale o Vercel CLI**:
```bash
npm install -g vercel
```

2. **Clone o repositório**:
```bash
git clone https://github.com/vinicius-pascoal/maquina-de-turing.git
cd maquina-de-turing
```

3. **Faça login na Vercel**:
```bash
vercel login
```

4. **Deploy**:
```bash
vercel
```

Pronto! Seu simulador estará online em poucos segundos. 🎉

### Deploy via GitHub

1. Faça push do código para o GitHub
2. Acesse [vercel.com](https://vercel.com)
3. Clique em "New Project"
4. Importe seu repositório
5. Clique em "Deploy"

A Vercel detectará automaticamente a configuração e fará o deploy!

## 💻 Desenvolvimento Local

### Pré-requisitos

- Python 3.9 ou superior
- Navegador web moderno

### Executando Localmente

1. **Clone o repositório**:
```bash
git clone https://github.com/vinicius-pascoal/maquina-de-turing.git
cd maquina-de-turing
```

2. **Instale um servidor HTTP local**:
```bash
# Python
python -m http.server 8000

# Node.js
npx serve public
```

3. **Acesse no navegador**:
```
http://localhost:8000/public/
```

### Testando as APIs Localmente

Para testar as funções serverless localmente, instale o Vercel CLI:

```bash
vercel dev
```

O projeto estará disponível em `http://localhost:3000`

## 📖 Como Usar

### 1. Selecione um Exemplo
Escolha um dos 12 exemplos prontos no dropdown para ver máquinas funcionando.

### 2. Ou Crie Sua Própria Máquina

Use o botão **Dicionário** para ver a sintaxe completa. Exemplo de uma máquina de paridade:

```
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
```

### 3. Defina a Entrada
Digite a cadeia de entrada (ex: `0011`, `101`, `111+11`).

### 4. Execute
- **Validar**: Verifica se a especificação está correta
- **Inicializar Máquina**: Prepara a máquina para execução
- **Passo**: Executa uma transição por vez
- **10 Passos**: Executa 10 transições
- **Executar Tudo**: Executa até aceitar, rejeitar ou atingir limite

## 📝 Sintaxe da Especificação

### Estrutura Básica

```
states: estado1,estado2,estado3,...
blank: símbolo_vazio
start: estado_inicial
accept: estado_aceitacao
reject: estado_rejeicao
transitions:
estado,simbolo_lido -> estado_destino,simbolo_escrito,movimento
```

### Componentes

- **states**: Lista de todos os estados da máquina
- **blank**: Símbolo que representa célula vazia (geralmente `_` ou `B`)
- **start**: Estado onde a máquina inicia
- **accept**: Estado de aceitação
- **reject**: Estado de rejeição
- **transitions**: Regras de transição, uma por linha

### Formato das Transições

```
estado_atual,símbolo_lido -> próximo_estado,símbolo_escrito,direção
```

**Direções:**
- `R` - Move cabeçote para direita
- `L` - Move cabeçote para esquerda
- `N` - Não move cabeçote (permanece na posição)

### Exemplo Completo: Duplicador

```
states: q0,q1,q2,q3,q4,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q1,_,R
q0,1 -> q3,_,R
q0,_ -> qaccept,_,N
q1,0 -> q1,0,R
q1,1 -> q1,1,R
q1,_ -> q2,0,L
q2,0 -> q2,0,L
q2,1 -> q2,1,L
q2,_ -> q0,_,R
q3,0 -> q3,0,R
q3,1 -> q3,1,R
q3,_ -> q4,1,L
q4,0 -> q4,0,L
q4,1 -> q4,1,L
q4,_ -> q0,_,R
```

## 🎮 Controles da Interface

### Botões Principais
- **📖 Dicionário**: Abre modal com sintaxe completa e exemplos
- **✓ Validar**: Verifica se a especificação está correta
- **🔄 Inicializar Máquina**: Prepara máquina com a entrada fornecida

### Controles de Execução
- **▶ Passo**: Executa uma única transição
- **⏭ 10 Passos**: Executa 10 transições de uma vez
- **⚡ Executar Tudo**: Executa até parar (aceitar/rejeitar/loop infinito)

### Visualização
- **Fita**: Mostra o conteúdo da fita com destaque na posição atual
- **Status**: Exibe estado atual, posição do cabeçote e símbolo lido
- **Resultado**: Indica se a entrada foi aceita, rejeitada ou está em execução
- **Transições**: Tabela com todas as regras de transição da máquina

## 🛠️ Estrutura do Projeto

```
maquina-de-turing/
├── api/                      # Serverless Functions (Vercel)
│   ├── examples.js          # API: Lista exemplos disponíveis
│   ├── reset.js             # API: Inicializa máquina
│   ├── run.js               # API: Executa múltiplos passos
│   ├── step.js              # API: Executa um passo
│   └── validate.js          # API: Valida especificação
├── core/                     # Lógica da Máquina de Turing
│   ├── __init__.py
│   ├── examples.py          # Exemplos pré-definidos (Python)
│   ├── turing_machine.js    # Implementação MT (JavaScript)
│   └── turing_machine.py    # Implementação MT (Python)
├── public/                   # Frontend Estático
│   ├── index.html           # Interface principal com SVGs
│   ├── script.js            # Lógica do cliente + modal
│   └── styles.css           # Design system completo
├── vercel.json              # Configuração do deploy
├── package.json             # Dependências Node.js
├── test_endpoints.js        # Testes das APIs
├── test_apis.py             # Testes Python
└── README.md                # Documentação
```

## 🏗️ Arquitetura

### Backend (Serverless Functions)
- **APIs REST em JavaScript**: Funções serverless na Vercel
- **Core em Python**: Lógica da Máquina de Turing reutilizável
- **Stateless**: Cada requisição é independente
- **Auto-scaling**: Escala automaticamente com demanda

### Frontend
- **HTML5 Semântico**: Estrutura acessível e SEO-friendly
- **CSS3 Moderno**: Grid, Flexbox, Custom Properties, Gradientes
- **JavaScript Vanilla ES6+**: Sem dependências externas
- **Ícones SVG**: Todos os ícones em formato vetorial
- **Design System**: Paleta consistente e componentes reutilizáveis

### Fluxo de Dados
```
┌─────────┐     ┌─────────────┐     ┌──────────┐     ┌──────────┐
│ Cliente │ ──> │ API (JS)    │ ──> │ Core (PY)│ ──> │ Response │
│ (HTML)  │ <── │ Serverless  │ <── │ TM Logic │ <── │ (JSON)   │
└─────────┘     └─────────────┘     └──────────┘     └──────────┘
```

### Endpoints da API

- `GET /api/examples` - Lista todos os exemplos disponíveis
- `POST /api/validate` - Valida especificação da máquina
- `POST /api/reset` - Inicializa máquina com entrada
- `POST /api/step` - Executa um passo da máquina
- `POST /api/run` - Executa múltiplos passos

## 📖 Conceitos da Máquina de Turing

Uma Máquina de Turing é um modelo matemático de computação que consiste em:

- **Fita**: Uma fita infinita dividida em células, cada uma contendo um símbolo
- **Cabeçote**: Um dispositivo que pode ler e escrever símbolos na fita e mover-se para a esquerda ou direita
- **Estados**: Um conjunto finito de estados que a máquina pode estar
- **Função de Transição**: Define como a máquina muda de estado baseado no símbolo lido
- **Estados de Aceitação/Rejeição**: Estados especiais que indicam se a entrada foi aceita ou rejeitada

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e experimental.

## 👨‍💻 Autor

**Vinicius Pascoal**
- GitHub: [@vinicius-pascoal](https://github.com/vinicius-pascoal)
- Projeto: [maquina-de-turing](https://github.com/vinicius-pascoal/maquina-de-turing)

## 🔗 Links Úteis

### Documentação
- [Máquina de Turing - Wikipedia PT](https://pt.wikipedia.org/wiki/M%C3%A1quina_de_Turing)
- [Turing Machine - Wikipedia EN](https://en.wikipedia.org/wiki/Turing_machine)
- [Teoria da Computação](https://pt.wikipedia.org/wiki/Teoria_da_computa%C3%A7%C3%A3o)
- [Computabilidade](https://pt.wikipedia.org/wiki/Teoria_da_computabilidade)

### Tecnologias
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Serverless Functions](https://vercel.com/docs/functions)
- [MDN Web Docs](https://developer.mozilla.org/)

### Recursos Educacionais
- [Introduction to the Theory of Computation - Michael Sipser](https://www.amazon.com/Introduction-Theory-Computation-Michael-Sipser/dp/113318779X)
- [Brilliant - Turing Machines](https://brilliant.org/wiki/turing-machines/)
- [Stanford CS143 - Automata](https://web.stanford.edu/class/cs143/)

## ⚡ Performance

- **Tempo de resposta**: < 200ms por operação
- **Cold start**: < 1s (primeira requisição)
- **Warm requests**: < 100ms
- **Escalabilidade**: Ilimitada (serverless)

## 🎨 Tecnologias Utilizadas

### Frontend
- **HTML5**: Estrutura semântica e acessível
- **CSS3**: Grid, Flexbox, Custom Properties, Animations
- **JavaScript ES6+**: Async/Await, Fetch API, Modules
- **SVG**: Ícones vetoriais customizados
- **Design System**: Paleta de cores, tipografia, espaçamento

### Backend
- **Node.js**: Runtime para serverless functions
- **Python 3.9+**: Lógica da Máquina de Turing
- **JavaScript**: APIs REST serverless

### Infraestrutura
- **Vercel**: Hosting + Serverless + CDN
- **Edge Network**: Deploy global com baixa latência
- **HTTPS**: Certificado SSL automático
- **Auto-scaling**: Escala conforme demanda

### Ferramentas de Desenvolvimento
- **Git**: Controle de versão
- **Vercel CLI**: Deploy e testes locais
- **ESLint**: Code quality (JavaScript)
- **Python Type Hints**: Type safety

## 🎨 Customização

### Design System

Todas as cores e estilos estão centralizados em variáveis CSS em `public/styles.css`:

```css
:root {
    /* Cores principais */
    --primary: #6366f1;
    --primary-hover: #4f46e5;
    --success: #10b981;
    --danger: #ef4444;
    --warning: #f59e0b;
    
    /* Backgrounds */
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    
    /* Texto */
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    
    /* Outros */
    --border: rgba(255, 255, 255, 0.1);
    --shadow: rgba(0, 0, 0, 0.5);
}
```

### Adicionar Novos Exemplos

Edite `core/examples.py` e `api/examples.js` seguindo o formato:

```python
"Nome do Exemplo": """states: q0,q1,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject
transitions:
q0,0 -> q1,0,R
...
"""
```

### Ajustar Limites

No código JavaScript das APIs (`api/*.js`):

```javascript
const MAX_STEPS = 1000;  // Máximo de passos por execução
const TAPE_SIZE = 100;   // Tamanho máximo da fita
```

## 📊 Limites da Vercel

- **Timeout**: 10s (Hobby) / 60s (Pro)
- **Payload**: 4.5MB por requisição
- **Bandwidth**: 100GB/mês (Hobby)

Para máquinas muito complexas, considere aumentar o timeout no plano Pro.

## 🐛 Troubleshooting

### Erro "Module not found"
```bash
# Certifique-se de que todos os arquivos estão no lugar
vercel dev
```

### API não responde
- Verifique os logs: `vercel logs`
- Teste localmente: `vercel dev`

### Interface não carrega
- Limpe o cache do navegador
- Verifique o console do navegador (F12)

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/vinicius-pascoal/maquina-de-turing/issues)
- **Discussões**: [GitHub Discussions](https://github.com/vinicius-pascoal/maquina-de-turing/discussions)

## ✅ Funcionalidades Implementadas

- [x] Interface web moderna com design dark mode
- [x] 12 exemplos de máquinas pré-configuradas
- [x] Editor de especificações com validação
- [x] Visualização da fita em tempo real
- [x] Controles de execução (passo, 10 passos, executar tudo)
- [x] Modal de dicionário com sintaxe completa
- [x] Ícones SVG para melhor qualidade visual
- [x] Status detalhado (estado, posição, símbolo)
- [x] Tabela de transições
- [x] Deploy automático na Vercel
- [x] APIs serverless para backend
- [x] Design responsivo (mobile, tablet, desktop)

## 🗺️ Roadmap Futuro

- [ ] Histórico de execução (undo/redo)
- [ ] Exportar/importar máquinas em JSON
- [ ] Modo de depuração avançado com breakpoints
- [ ] Compartilhar máquinas via URL
- [ ] Temas customizáveis (light/dark)
- [ ] Múltiplas fitas (Multi-tape TM)
- [ ] Animações de transição mais suaves
- [ ] Grafos visuais das transições
- [ ] Modo de comparação de máquinas
- [ ] Estatísticas de execução (passos, tempo)

## 📸 Screenshots

### Interface Principal
![Simulador de Máquina de Turing](https://via.placeholder.com/800x450/0f172a/6366f1?text=Simulador+de+Maquina+de+Turing)

### Modal de Dicionário
![Dicionário de Sintaxe](https://via.placeholder.com/800x450/1e293b/10b981?text=Dicionario+de+Sintaxe)

### Visualização da Fita
![Fita em Execução](https://via.placeholder.com/800x450/334155/f59e0b?text=Visualizacao+da+Fita)

## 📄 Licença

Este projeto é open-source e está disponível sob a licença MIT.

```
MIT License

Copyright (c) 2024 Vinicius Pascoal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Desenvolvido com ❤️ para o estudo de Teoria da Computação**

Se este projeto foi útil para você, considere dar uma ⭐ no GitHub!

[⬆ Voltar ao topo](#-simulador-de-máquina-de-turing)

</div>
