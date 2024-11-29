# Linguagem Fictícia para Python - Compilador

Este projeto implementa um compilador para uma linguagem fictícia criada para fins educacionais. O compilador traduz programas escritos nesta linguagem para código Python executável. Ele é composto por módulos responsáveis por análise léxica, análise sintática, análise semântica e geração de código Python.

# Estrutura do Projeto

Arquivos do Projeto

# main.py

O ponto de entrada do programa. Este arquivo:

Lê um arquivo de entrada contendo o código-fonte na linguagem fictícia.
Realiza o processo de tokenização, análise sintática e geração de código Python.
Salva o código Python gerado em um arquivo e o executa automaticamente.

# lexer.py

Responsável pela análise léxica, onde o código-fonte é transformado em uma sequência de tokens. Cada token representa uma unidade sintática válida, como palavras-chave, identificadores, operadores, etc.

# parser.py

Realiza a análise sintática e semântica do programa:

Garante que o código-fonte segue as regras gramaticais da linguagem.
Verifica a existência e compatibilidade de tipos de variáveis.
Gera o código Python equivalente.

# meu_programa.txt

Um exemplo de programa escrito na linguagem fictícia. Este arquivo demonstra como utilizar os principais comandos da linguagem.

# output.py

Arquivo gerado pelo compilador contendo o código Python traduzido a partir do programa de entrada.

# Como Usar

Requisitos

Python 3.8 ou superior.

# Execução

Certifique-se de que todos os arquivos necessários (main.py, lexer.py, parser.py, meu_programa.txt) estão no mesmo diretório.
Abra um terminal no diretório onde os arquivos estão localizados.
Execute o comando abaixo.

python main.py meu_programa.txt

O código Python gerado será salvo no arquivo output.py.
O programa gerado será automaticamente executado, e os resultados serão exibidos no terminal.

# Exemplo

# Entrada (meu_programa.txt)

inicioDoPrograma
inteiro numero|
inteiro fatorial|
inteiro contador|

    escreva("Digite um número para calcular o fatorial:")|
    leia(numero)|

    fatorial recebe 1|
    contador recebe 1|

    enquanto (contador menor_igual numero) {
        fatorial recebe fatorial vezes contador|
        contador recebe contador mais 1|
    }

    escreva("O fatorial de")|
    escreva(numero)|
    escreva("é:")|
    escreva(fatorial)|

fimDoPrograma

# Saída Gerada (output.py)

numero = 0 # int
fatorial = 0 # int
contador = 0 # int
print("Digite um número para calcular o fatorial:")
numero = int(input())
fatorial = 1
contador = 1
while contador <= numero:
fatorial = (fatorial \* contador)
contador = (contador + 1)
print("O fatorial de")
print(numero)
print("é:")
print(fatorial)

# Execução

Ao executar o programa, o terminal exibirá algo como:

Digite um número para calcular o fatorial:
5
O fatorial de
5
é:
120

# Comandos da Linguagem Fictícia

A linguagem fictícia suporta os seguintes comandos:

# Declaração de Variáveis

inteiro variavel|
decimal variavel|
texto variavel|

# Entrada de Dados

leia(variavel)|

# Saída de Dados

escreva("texto")|
escreva(variavel)|

# Atribuição

variavel recebe expressão|

# Laços e Condicionais

Enquanto
enquanto (condição) {
// código
}

# Se

dadoQue (condição) {
// código
}

# Operadores Suportados

Relacionais: menor, maior, igual, diferente, menor_igual, maior_igual
Aritméticos: mais, menos, vezes, dividido, modulo

# Estrutura Interna

Fases do Compilador

Tokenização (lexer.py)

Converte o código-fonte em tokens.
Análise Sintática e Semântica (parser.py)

Verifica a estrutura do programa e a compatibilidade de tipos.
Geração de Código (parser.py)

Traduz o programa da linguagem fictícia para Python.
