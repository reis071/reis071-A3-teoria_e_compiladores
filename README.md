# A3 teoria e compiladores

Analisador Léxico tradutor de linguagem própria para Python

Autores:
Guilherme Reis correia 12722123056    
Luís Carlos Santos Melo de Jesus 1272122545 
Luan Cavalcante Dias Rodrigues 1272122479   
Victor Hugo Cordeiro   1272123431   
Victor Macedo Camargo  1271924581   

Descrição

Esse Projeto tem como Objetivo traduzir o código de uma linguagem própria para o Python, iniciando com a fase de análise léxica, que identifica os componentes básicos do código.
o projeto implementa um compilador para uma linguagem fictícia criada para fins educacionais. O compilador traduz programas escritos nesta linguagem para código Python executável. Ele é composto por módulos responsáveis por análise léxica, análise sintática, análise semântica e geração de código Python.



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

# main.py
# Arquivo principal para a execução do compilador de linguagem fictícia.
# Este programa lê um arquivo contendo código na linguagem fictícia, compila para Python e executa o código gerado.

O ponto de entrada do programa. Este arquivo:
Lê um arquivo de entrada contendo o código-fonte na linguagem fictícia.
Realiza o processo de tokenização, análise sintática e geração de código Python.
Salva o código Python gerado em um arquivo e o executa automaticamente.

    import sys
    from lexer import tokenize
    from parser import Parser

    def read_code(file_path):
        """Lê o código do arquivo fornecido pelo usuário.

        Args:
            file_path (str): Caminho do arquivo de entrada.

        Returns:
            str: Conteúdo do código como string.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def compile_to_python(code):
        """Compila o código da linguagem fictícia para Python.

        Args:
            code (str): Código na linguagem fictícia.

        Returns:
            str: Código equivalente em Python.
        """
        tokens = tokenize(code)  # Tokeniza o código
        parser = Parser(tokens)  # Cria o parser com os tokens
        return parser.parse()  # Retorna o código Python gerado

    def save_and_run(generated_code, output_file='output.py'):
        """Salva o código Python gerado e o executa.

        Args:
            generated_code (str): Código gerado em Python.
            output_file (str, optional): Nome do arquivo para salvar o código gerado. Padrão é 'output.py'.
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(generated_code)

        print("Executando o código...")
        with open(output_file, 'r', encoding='utf-8') as file:
            exec(file.read())

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Uso: python main.py <arquivo_de_entrada>")
            sys.exit(1)

        input_file = sys.argv[1]  # Arquivo de entrada fornecido pelo usuário

        # Lê e compila o código da linguagem fictícia para Python
        code = read_code(input_file)
        generated_code = compile_to_python(code)

        # Salva e executa o código Python gerado
        save_and_run(generated_code)

# lexer.py

# Lexer para a linguagem fictícia.

# Responsável por transformar o código de entrada em uma lista de tokens, que serão analisados pelo parser.
Responsável pela análise léxica, onde o código-fonte é transformado em uma sequência de tokens. Cada token representa uma unidade sintática válida, como palavras-chave, identificadores, operadores, etc.

    import re

    #Definição dos tokens da linguagem

    tokens_definitions = {
        'PROGRAM': r'\binicioDoPrograma\b',
        'END_PROGRAM': r'\bfimDoPrograma\b',
        'INT': r'\binteiro\b',
        'DECIMAL': r'\bdecimal\b',
        'TEXT': r'\btexto\b',
        'IF': r'\bdadoQue\b',
        'ELSE': r'\bsenao\b',
        'WHILE': r'\benquanto\b',
        'FOR': r'\bparaCada\b',
        'READ': r'\bleia\b',
        'WRITE': r'\bescreva\b',
        'ASSIGN': r'recebe',
        'REL_OP': r'igual|diferente|menor|maior|menor_igual|maior_igual',
        'ADD_OP': r'mais|menos',
        'MUL_OP': r'vezes|dividido',
        'LPAREN': r'\(',
        'RPAREN': r'\)',
        'LBRACE': r'\{',
        'RBRACE': r'\}',
        'COMMA': r',',
        'SEMI': r';',
        'DOT': r'\.',  # Token para ponto final
        'NUMBER': r'\d+(\.\d+)?',
        'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'STRING': r'"[^"]*"',  # Corrigido para permitir strings
        'NEWLINE': r'\n',
        'WHITESPACE': r'[ \t]+',
    }

    def lex(code):
        """Transforma o código de entrada em tokens.

        Args:
        code (str): Código da linguagem fictícia.

        Returns:
            list[tuple]: Lista de tokens como (tipo, valor).

        Raises:
            SyntaxError: Caso encontre um caractere inesperado.
        """
    tokens_found = []
    position = 0
    while position < len(code):
        match = None
        for token_type, pattern in tokens_definitions.items():
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                text = match.group(0)
                if token_type not in ['WHITESPACE', 'NEWLINE']:  # Ignora espaços e novas linhas
                    tokens_found.append((token_type, text))
                position = match.end(0)
                break
        if not match:
            raise SyntaxError(f'Erro Léxico: caractere inesperado {code[position]} na posição {position}')
    return tokens_found

    def tokenize(code):
        """Função principal para tokenização.

        Args:
            code (str): Código da linguagem fictícia.

        Returns:
            list[tuple]: Lista de tokens encontrados.
        """
        return lex(code)

    def test_lexer():
        """Teste simples para o lexer, usando um exemplo de código."""
        test_code = '''
        inicioDoPrograma
        inteiro a, b.
        decimal d.
        escreva("Bem-vindo à linguagem fictícia").
        leia(a).
        dadoQue (a menor b) {
            c recebe a mais b.
        } senao {
            c recebe a menos b.
        }
        paraCada (i recebe 0; i menor 10; i recebe i mais 1) {
            escreva(i).
        }
        fimDoPrograma
        '''

        try:
            tokens = tokenize(test_code)
            for token in tokens:
                print(token)
        except SyntaxError as e:
            print(e)

    if __name__ == "__main__":
        test_lexer()

# parser.py
# O parser.py é responsável por realizar a análise sintática do código tokenizado, utilizando a gramática da linguagem fictícia, além de gerar código equivalente em Python. Ele também realiza uma análise semântica básica, como validação de declarações e compatibilidade de tipos.

# 1. Classe CodeGenerator
# A classe CodeGenerator gerencia a geração do código Python a partir da análise sintática.
Realiza a análise sintática e semântica do programa:
Garante que o código-fonte segue as regras gramaticais da linguagem.
Verifica a existência e compatibilidade de tipos de variáveis.
Gera o código Python equivalente.

    class CodeGenerator:
        def __init__(self):
            self.code = []
            self.indent_level = 0

        def add_line(self, line):
            indent = '    ' * self.indent_level
            self.code.append(f"{indent}{line}")

        def increase_indent(self):
            self.indent_level += 1

        def decrease_indent(self):
            if self.indent_level > 0:
                self.indent_level -= 1

        def get_code(self):
            return "\n".join(self.code)
# 2. Classe SemanticAnalyzer
# A classe SemanticAnalyzer realiza verificações semânticas no código, como validação de variáveis e tipos.

    class SemanticAnalyzer:
        def __init__(self):
            self.symbol_table = {}

        def declare_variable(self, name, var_type):
            if name in self.symbol_table:
                raise ValueError(f"Erro Semântico: Variável '{name}' já foi declarada.")
            self.symbol_table[name] = var_type

        def check_variable(self, name):
            if name not in self.symbol_table:
                raise ValueError(f"Erro Semântico: Variável '{name}' não foi declarada.")
            return self.symbol_table[name]

        def check_type_compatibility(self, var_name, expression_type):
            var_type = self.check_variable(var_name)
            if var_type != expression_type:
                raise ValueError(f"Erro Semântico: Tipo incompatível para '{var_name}', esperado '{var_type}' mas obteve '{expression_type}'.")

            
# 3. Classe Parser
# A classe Parser realiza a análise sintática do código tokenizado e utiliza as classes CodeGenerator e SemanticAnalyzer para gerar código Python e realizar validações.

    class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.generator = CodeGenerator()
        self.semantic_analyzer = SemanticAnalyzer()

    def match(self, expected_type):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == expected_type:
            self.position += 1
            return True
        else:
            return False

    def error(self, message="Erro de Sintaxe"):
        raise SyntaxError(f"{message} no token {self.tokens[self.position]} na posição {self.position}")

    def parse(self):
        self.program()
        return self.generator.get_code()
# 4. Funções do Parser
# Função Principal: program()
# Analisa a estrutura principal do programa, verificando o início e o fim.

    def program(self):
        if not self.match('PROGRAM'):
            self.error("Esperado 'inicioDoPrograma'")
        self.declara()
        self.bloco()
        if not self.match('END_PROGRAM'):
            self.error("Esperado 'fimDoPrograma'")

# Declaração de Variáveis: declara()
# Analisa declarações de variáveis e gera as inicializações correspondentes.

    def declara(self):
        while self.tokens[self.position][0] in ['INT', 'DECIMAL', 'TEXT']:
            tipo = self.tipo()
            ids = self.id_list()
            for var in ids:
                self.semantic_analyzer.declare_variable(var, tipo)
                if tipo == "inteiro":
                    self.generator.add_line(f"{var} = 0  # int")
                elif tipo == "decimal":
                    self.generator.add_line(f"{var} = 0.0  # float")
                elif tipo == "texto":
                    self.generator.add_line(f"{var} = ''  # str")
            if not self.match('DOT'):
                self.error("Esperado '.' após declaração")

# Estruturas Condicionais: cmd_if()
# Processa condições (dadoQue) e blocos opcionais (senao).

    def cmd_if(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'dadoQue'")

        left_expr = self.expr()

        if not self.match('REL_OP'):
            self.error("Operador relacional esperado em 'dadoQue'")

        operador = self.tokens[self.position - 1][1]
        operador_python = self.parse_operador_relacional(operador)

        right_expr = self.expr()
        condition = f"{left_expr} {operador_python} {right_expr}"

        if not self.match('RPAREN'):
            self.error("Esperado ')' após expressão em 'dadoQue'")

        if not self.match('LBRACE'):
            self.error("Esperado '{' após condição 'dadoQue'")

        self.generator.add_line(f"if {condition}:")
        self.generator.increase_indent()
        self.bloco()
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'dadoQue'")

        if self.match('ELSE'):
            if not self.match('LBRACE'):
                self.error("Esperado '{' após 'senao'")
            self.generator.add_line("else:")
            self.generator.increase_indent()
            self.bloco()
            self.generator.decrease_indent()
            if not self.match('RBRACE'):
                self.error("Esperado '}' após bloco 'senao'")
            
# Loop paraCada: cmd_para()
# Processa loops utilizando o comando paraCada.

    def cmd_para(self):
        if not self.match('FOR'):
            self.error("Esperado 'paraCada'")

        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'paraCada'")

        init_code = self.cmd_expr(for_loop=True)

        if not self.match('SEMI'):
            self.error("Esperado ';' após inicialização em 'paraCada'")

        condition = self.expr()

        if not self.match('SEMI'):
            self.error("Esperado ';' após condição em 'paraCada'")

        increment_code = self.cmd_expr(for_loop=True)

        if not self.match('RPAREN'):
            self.error("Esperado ')' após incremento em 'paraCada'")

        if not self.match('LBRACE'):
            self.error("Esperado '{' após 'paraCada'")

        self.generator.add_line(f"{init_code}  # Inicialização")
        self.generator.add_line(f"while {condition}:")
        self.generator.increase_indent()
        self.generator.add_line(f"{increment_code}")
        self.bloco()
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'paraCada'")
        
# Expressões: expr() e termo()
# Processam expressões matemáticas e termos.

    def expr(self):
        left_code, left_type = self.termo()
        while self.match('ADD_OP'):
            op = self.tokens[self.position - 1][1]
            op_python = self.parse_operador_matematico(op)
            right_code, right_type = self.termo()
            left_code = f"({left_code} {op_python} {right_code})"
            left_type = "decimal" if left_type == "decimal" or right_type == "decimal" else "inteiro"
        return left_code

    def termo(self):
        left_code, left_type = self.fator()
        while self.match('MUL_OP'):
            op = self.tokens[self.position - 1][1]
            op_python = self.parse_operador_matematico(op)
            right_code, right_type = self.fator()
            left_code = f"({left_code} {op_python} {right_code})"
            left_type = "decimal" if left_type == "decimal" or right_type == "decimal" else "inteiro"
        return left_code, left_type

Contribuições são bem-vindas! Para contribuir, por favor, siga as seguintes etapas:

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

Fork este repositório.  
Crie um novo branch para suas alterações.   
Faça o commit das suas alterações.  
Envie um pull request.  



