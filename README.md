# A3-teoria_e_compiladores

Analisador Léxico tradutor de linguagem própria para Python

Autores:
Guilherme Reis
Luis
Luan
Victor Hugo
Victor Macedo Camargo   RA: 1271924581

Descrição

Esse Projeto tem como Objetivo traduzir o código de uma linguagem própria para o Python, iniciando com a fase de análise léxica, que identifica os componentes básicos do código.


Instalação

Python 3.12 ou superior deve estar instalado na maquina
Clone o repositório

Para executar o analisador, é necessario rodar o "meu_programa.txt" na raiz do repositório

Estrutura dos Arquivos

main.py: Ponto de entrada do programa.
lexer.py: Contém a definição dos tokens e as regras léxicas.
parser.py: (Futuro) Contará as regras gramaticais da linguagem.
tokens.py: (Opcional) Arquivo separado para definir os tokens.

Tokens suportados:

inicioDoPrograma
fimDoPrograma
inteiro
decimal
texto
dadoQue
senao
enquanto
paraCada
leia
escreva
recebe
igual|diferente|menor|maior|menor_igual|maior_igual
mais|menos
vezes|dividido
\(
\)
\{
\}   
,
;
\.
\d+(\.\d+)?
[a-zA-Z_][a-zA-Z0-9_]*
"[^"]*"
\n
[ \t]+



Exemplo de uso: 

inicioDoPrograma
    inteiro i.
    escreva("Contando de 0 a 9:").
    
    paraCada (i recebe 0; i menor 10; i recebe i mais 1) {
        escreva(i).
    }
    
fimDoPrograma

Contribuições são bem-vindas! Para contribuir, por favor, siga as seguintes etapas:

Fork este repositório.
Crie um novo branch para suas alterações.
Faça o commit das suas alterações.
Envie um pull request.

