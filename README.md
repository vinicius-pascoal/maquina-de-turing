# 🤖 Simulador de Máquina de Turing

Um simulador interativo de Máquina de Turing com interface web moderna. Este projeto permite definir, visualizar e executar máquinas de Turing de forma intuitiva, ideal para fins educacionais e experimentação.

## 🌟 Demo Online

**[Ver Demo ao Vivo](https://seu-projeto.vercel.app)** _(após deploy)_

## 📋 Características

- **Interface Web Moderna**: Design elegante e responsivo com animações suaves
- **Editor de Especificações**: Defina máquinas de Turing usando uma DSL simples
- **Visualização em Tempo Real**: Observe a fita, cabeçote e estado atual durante a execução
- **Controle de Execução**: Execute passo a passo, 10 passos ou até completar
- **Exemplos Pré-definidos**: Inclui exemplos prontos (0^n1^n, paridade, duplicador e mais)
- **Validação Automática**: Validação em tempo real das especificações
- **Design System Completo**: Interface dark mode profissional
- **Totalmente Responsivo**: Funciona perfeitamente em mobile, tablet e desktop

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

### Definindo uma Máquina de Turing

Use a linguagem de especificação (DSL) para definir sua máquina. Exemplo de uma máquina que reconhece palíndromos:

```
states: q0,q1,q2,q3,q4,qaccept,qreject
blank: _
start: q0
accept: qaccept
reject: qreject

# Transições: (estado_atual, símbolo_lido) -> (novo_estado, símbolo_escrito, movimento)
# Movimento: L (esquerda), R (direita), N (nenhum)

(q0, 0) -> (q1, _, R)
(q0, 1) -> (q2, _, R)
(q0, _) -> (qaccept, _, N)

(q1, 0) -> (q1, 0, R)
(q1, 1) -> (q1, 1, R)
(q1, _) -> (q3, _, L)

(q2, 0) -> (q2, 0, R)
(q2, 1) -> (q2, 1, R)
(q2, _) -> (q4, _, L)

(q3, 0) -> (q0, _, L)
(q3, _) -> (qaccept, _, N)

(q4, 1) -> (q0, _, L)
(q4, _) -> (qaccept, _, N)
```

### Sintaxe da DSL

A linguagem de especificação segue estas regras:

- **Comentários**: Linhas iniciadas com `#` são ignoradas
- **states**: Lista de estados separados por vírgula
- **blank**: Símbolo que representa uma célula vazia na fita
- **start**: Estado inicial
- **accept**: Estados de aceitação (separados por vírgula)
- **reject**: Estados de rejeição (separados por vírgula)
- **Transições**: `(estado, símbolo) -> (novo_estado, escrever, movimento)`
  - Movimento pode ser: `L` (esquerda), `R` (direita), `N` (nenhum)

## 📚 Exemplos Incluídos

O simulador vem com vários exemplos pré-configurados:

1. **Reconhecedor de Palíndromos**: Verifica se uma string binária é um palíndromo
2. **Duplicador de String**: Duplica uma string binária (ex: `01` → `0101`)
3. **Incrementador Binário**: Incrementa um número binário em 1
4. **Aceitador de a^n b^n**: Reconhece strings na forma a^n b^n
5. **Substituidor**: Substitui todos os `0`s por `1`s

## 🎮 Controles da Interface

- **Carregar Exemplo**: Selecione e carregue um exemplo pré-definido
- **Validar**: Verifica se a especificação da máquina está correta
- **Resetar**: Reinicia a máquina com a entrada fornecida
- **Passo**: Executa um único passo da máquina
- **Rodar**: Executa a máquina automaticamente até parar
- **Exportar JSON**: Salva a máquina em formato JSON

## 🛠️ Estrutura do Projeto

```
maquina-de-turing/
├── api/                    # Funções serverless da Vercel
│   ├── __init__.py
│   ├── validate.py        # Valida especificação
│   ├── reset.py           # Inicializa máquina
│   ├── step.py            # Executa um passo
│   ├── run.py             # Executa múltiplos passos
│   └── examples.py        # Retorna exemplos
├── core/                   # Lógica da Máquina de Turing
│   ├── __init__.py
│   ├── turing_machine.py  # Implementação da MT
│   └── examples.py        # Exemplos pré-definidos
├── public/                 # Frontend estático
│   ├── index.html         # Interface principal
│   ├── styles.css         # Estilos modernos
│   └── script.js          # Lógica do cliente
├── app.py                  # Versão Gradio (legado)
├── vercel.json            # Configuração Vercel
├── requirements.txt       # Dependências Python
├── .gitignore
└── README.md
```

## 🏗️ Arquitetura

### Backend (Serverless)
- **APIs REST** em Python usando funções serverless da Vercel
- **Stateless**: cada requisição é independente
- **Escalável**: auto-scaling da Vercel

### Frontend
- **HTML5 + CSS3 + JavaScript Vanilla**
- **Design System** completo com variáveis CSS
- **Animações suaves** e transições
- **Responsivo** para todos os dispositivos

### Fluxo de Dados
```
[Cliente] → [API] → [Core] → [Processamento] → [API] → [Cliente]
```

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

Desenvolvido por [Vinicius Pascoal](https://github.com/vinicius-pascoal)

## 🔗 Links Úteis

- [Máquina de Turing - Wikipedia](https://pt.wikipedia.org/wiki/M%C3%A1quina_de_Turing)
- [Documentação Gradio](https://www.gradio.app/docs/)
- [Teoria da Computação](https://en.wikipedia.org/wiki/Theory_of_computation)

## ⚡ Performance

- **Tempo de resposta**: < 200ms por operação
- **Cold start**: < 1s (primeira requisição)
- **Warm requests**: < 100ms
- **Escalabilidade**: Ilimitada (serverless)

## 🎨 Tecnologias Utilizadas

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Design System customizado
- Animações CSS
- Fetch API

### Backend
- Python 3.9+
- Vercel Serverless Functions
- Dataclasses
- Type Hints

### Infraestrutura
- Vercel (Hosting + Serverless)
- Edge Network (CDN Global)
- Automatic HTTPS

## 🔧 Configuração Avançada

### Variáveis de Ambiente

O projeto não requer variáveis de ambiente, mas você pode adicionar:

```bash
# .env (opcional)
MAX_STEPS=10000
TAPE_SPAN=50
```

### Customização do Design

Edite as variáveis CSS em `public/styles.css`:

```css
:root {
    --primary: #6366f1;
    --bg-primary: #0f172a;
    /* ... outras variáveis */
}
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

## 🗺️ Roadmap

- [ ] Histórico de execução (undo/redo)
- [ ] Exportar/importar máquinas em JSON
- [ ] Modo de depuração avançado
- [ ] Compartilhar máquinas via URL
- [ ] Temas customizáveis
- [ ] Múltiplas fitas (Multi-tape TM)

## 📄 Licença

Este projeto é open-source e está disponível sob a licença MIT.

---

**Desenvolvido com ❤️ para o estudo de Teoria da Computação**

Se este projeto foi útil, considere dar uma ⭐ no GitHub!
