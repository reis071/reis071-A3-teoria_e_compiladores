# 🖥️ A3 teoria e compiladores

## 📝 Descrição

Este projeto implementa um **compilador de linguagem fictícia** desenvolvido em Python. Ele traduz programas escritos em uma linguagem definida pelo grupo para código Python executável. O compilador realiza as seguintes etapas:

- **Análise Léxica**: Identifica os tokens no código-fonte.
- **Análise Sintática**: Verifica a estrutura do código com base nas regras gramaticais.
- **Análise Semântica**: Valida declarações, tipos e compatibilidade.
- **Geração de Código**: Produz código Python equivalente e executável.

---

## 📑 Tabela de Conteúdos

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Execução do Projeto](#execução-do-projeto)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Tokens Suportados](#tokens-suportados)
- [Gramática BNF](#gramática-bnf)
- [Demonstração](#demonstração)

---

## 🚀 Funcionalidades

- **Suporte a Tipos de Variáveis**:
  - Inteiro, Decimal, Texto, Booleano.
- **Estruturas de Controle**:
  - Condicional `dadoQue ... senao`.
  - Laços `enquanto` e `paraCada`.
- **Operadores**:
  - Aritméticos: `mais`, `menos`, `vezes`, `dividido`, `modulo`.
  - Relacionais: `menor`, `maior`, `igual`, `diferente`, `menor_igual`, `maior_igual`.
  - Lógicos: `e`, `ou`.
- **Comandos**:
  - `leia` para entrada de dados.
  - `escreva` para saída de dados.
- **Conversão para Python**:
  - Código convertido é funcional e executável.

---

## 🧰 Requisitos

Certifique-se de ter instalado:

- [Python 3.12+](https://www.python.org/downloads/).
- Um editor de texto ou IDE, como VSCode ou PyCharm.

---

## 🛠️ Configuração do Ambiente

1. Clone o repositório:

   ```bash
   git clone <URL do Repositório>
   cd <Nome do Repositório>
   ```

2. Certifique-se de que o arquivo `meu_programa.txt` esteja na raiz do repositório.

---

## ▶️ Execução do Projeto

1. Execute o arquivo principal:

   ```bash
   python main.py meu_programa.txt
   ```

2. O código Python gerado será salvo como `output.py` e executado automaticamente.

---

## 📂 Estrutura de Arquivos

- **`main.py`**: Ponto de entrada do programa. Lê o arquivo de entrada, realiza análise léxica, sintática e semântica, e gera o código Python.
- **`lexer.py`**: Realiza a análise léxica, transformando o código em uma sequência de tokens.
- **`parser.py`**: Análise sintática e semântica. Gera o código Python equivalente.
- **`gramatica.bnf`**: Contém a definição da gramática formal da linguagem fictícia.
- **`meu_programa.txt`**: Exemplo de código escrito na linguagem fictícia.
- **`output.py`**: Código Python gerado após a compilação.

---

## 🔤 Tokens Suportados

| Token                  | Descrição                                                |
| ---------------------- | -------------------------------------------------------- |
| `inicioDoPrograma`     | Início do programa                                       |
| `fimDoPrograma`        | Fim do programa                                          |
| `inteiro`              | Tipo inteiro                                             |
| `decimal`              | Tipo decimal                                             |
| `texto`                | Tipo texto                                               |
| `booleano`             | Tipo booleano                                            |
| `verdadeiro`           | Valor booleano true                                      |
| `falso`                | Valor booleano false                                     |
| `dadoQue`              | Condicional IF                                           |
| `senao`                | Condicional ELSE                                         |
| `enquanto`             | Laço WHILE                                               |
| `paraCada`             | Laço FOR                                                 |
| `leia`                 | Entrada de dados                                         |
| `escreva`              | Saída de dados                                           |
| `recebe`               | Operador de atribuição                                   |
| `modulo`               | Operador de módulo                                       |
| Operadores Relacionais | menor, maior, igual, diferente, menor_igual, maior_igual |
| Operadores Lógicos     | e, ou                                                    |
| Operadores Aritméticos | mais, menos, vezes, dividido                             |

---

## 📚 Gramática BNF

```bnf
<programa> ::= "inicioDoPrograma" <declarações> <bloco> "fimDoPrograma"
<declarações> ::= (<declaração>)*
<declaração> ::= ("inteiro" | "decimal" | "texto" | "booleano") <identificadores> "|"
<bloco> ::= (<comando>)*
<comando> ::= <comando_leitura> | <comando_escrita> | <comando_atribuicao> | <comando_condicional> | <comando_enquanto> | <comando_para>
```

---

## 💻 Demonstração

### Código de Entrada

Arquivo: `meu_programa.txt`

```plaintext
inicioDoPrograma

inteiro contador, maximo |
decimal preco, desconto |
texto mensagem |
booleano ativo |

contador recebe 0 |
maximo recebe 10 |
preco recebe 100.0 |
desconto recebe 0.2 |
mensagem recebe "Bem-vindo ao programa!" |
ativo recebe verdadeiro |

escreva(mensagem) |

dadoQue (ativo igual verdadeiro) {
    escreva("O programa está ativo.") |
} senao {
    escreva("O programa está desativado.") |
}

enquanto (contador menor maximo) {
    escreva("Contador atual: ") |
    escreva(contador) |
    contador recebe contador mais 1 |
}

paraCada (contador recebe 0; contador menor maximo; contador recebe contador mais 1) {
    escreva("Iteração do paraCada: ") |
    escreva(contador) |
}

preco recebe preco menos (preco vezes desconto) |
escreva("Preço com desconto: ") |
escreva(preco) |

escreva("Digite um número inteiro: ") |
leia(contador) |
escreva("Você digitou: ") |
escreva(contador) |

dadoQue (contador maior 0) {
    escreva("O número digitado é positivo.") |
} senao {
    escreva("O número digitado é zero ou negativo.") |
}

fimDoPrograma
```

### Saída Gerada

Arquivo: `output.py`

```python
contador = 0  # int
maximo = 0  # int
preco = 0.0  # float
desconto = 0.0  # float
mensagem = ''  # str
ativo = False  # bool
contador = 0
maximo = 10
preco = 100.0
desconto = 0.2
mensagem = "Bem-vindo ao programa!"
ativo = True
print(mensagem)
if ativo == True:
    print("O programa está ativo.")
else:
    print("O programa está desativado.")
while contador < maximo:
    print("Contador atual: ")
    print(contador)
    contador = (contador + 1)
contador = 0
while contador < maximo:
    print("Iteração do paraCada: ")
    print(contador)
    contador = (contador + 1)
preco = (preco - ((preco * desconto)))
print("Preço com desconto: ")
print(preco)
print("Digite um número inteiro: ")
contador = int(input())
print("Você digitou: ")
print(contador)
if contador > 0:
    print("O número digitado é positivo.")
else:
    print("O número digitado é zero ou negativo.")
```

---

## 📧 Autores

Guilherme Reis correia 12722123056

Luís Carlos Santos Melo de Jesus 1272122545

Luan Cavalcante Dias Rodrigues 1272122479

Victor Hugo Cordeiro 1272123431

Victor Macedo Camargo 1271924581

---
