# 🤖 Simulador de Máquina de Turing

Um simulador interativo de Máquina de Turing com interface web construída com Gradio. Este projeto permite definir, visualizar e executar máquinas de Turing de forma intuitiva, ideal para fins educacionais e experimentação.

## 📋 Características

- **Interface Web Interativa**: Interface moderna e responsiva usando Gradio
- **Editor de Especificações**: Defina máquinas de Turing usando uma DSL simples
- **Visualização em Tempo Real**: Observe a fita, cabeçote e estado atual durante a execução
- **Controle de Execução**: Execute passo a passo ou rode automaticamente
- **Exemplos Pré-definidos**: Inclui exemplos prontos como reconhecedor de palíndromos, duplicador, incrementador e mais
- **Validação de Sintaxe**: Validação automática das especificações da máquina
- **Exportação**: Salve suas máquinas em formato JSON

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone o repositório:
```bash
git clone https://github.com/vinicius-pascoal/maquina-de-turing.git
cd maquina-de-turing
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install gradio
```

## 💻 Uso

### Executando o Simulador

Para iniciar o simulador, execute:

```bash
python app.py
```

O servidor será iniciado e você poderá acessar a interface em: `http://127.0.0.1:7860`

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

## 🛠️ Estrutura do Código

```
maquina-de-turing/
├── app.py              # Código principal do simulador
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Esta documentação
```

### Componentes Principais

- **TuringMachine**: Classe que implementa a lógica da Máquina de Turing
- **Parser DSL**: Converte a especificação textual em uma máquina executável
- **Interface Gradio**: Interface web interativa para visualização e controle

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

## 🐛 Problemas Conhecidos

Se encontrar algum problema, por favor abra uma issue no GitHub.

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório do GitHub.

---

**Nota**: Este é um projeto educacional para demonstração dos conceitos de Máquinas de Turing. Divirta-se explorando os limites da computabilidade!
