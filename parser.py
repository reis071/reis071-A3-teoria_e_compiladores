from lexer import tokenize  # Importando a função do lexer

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def add_line(self, line):
        indent = '    ' * self.indent_level  # Quatro espaços por nível de indentação
        self.code.append(f"{indent}{line}")

    def increase_indent(self):
        self.indent_level += 1

    def decrease_indent(self):
        if self.indent_level > 0:
            self.indent_level -= 1

    def get_code(self):
        return "\n".join(self.code)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Guarda variáveis e seus tipos

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

    # Função principal do programa
    def program(self):
        if not self.match('PROGRAM'):
            self.error("Esperado 'inicioDoPrograma'")
        self.declara()
        self.bloco()
        if not self.match('END_PROGRAM'):
            self.error("Esperado 'fimDoPrograma'")

    # Função para declaração de variáveis
    def declara(self):
        while self.tokens[self.position][0] in ['INT', 'DECIMAL', 'TEXT']:
            tipo = self.tipo()
            ids = self.id_list()
            for var in ids:
                self.semantic_analyzer.declare_variable(var, tipo)  # Declaração de variáveis para análise semântica
                if tipo == "inteiro":
                    self.generator.add_line(f"{var} = 0  # int")
                elif tipo == "decimal":
                    self.generator.add_line(f"{var} = 0.0  # float")
                elif tipo == "texto":
                    self.generator.add_line(f"{var} = ''  # str")
            if not self.match('DOT'):
                self.error("Esperado '.' após declaração")

    def tipo(self):
        if self.match('INT'):
            return "inteiro"
        elif self.match('DECIMAL'):
            return "decimal"
        elif self.match('TEXT'):
            return "texto"
        else:
            self.error("Tipo de variável esperado")

    def id_list(self):
        ids = []
        if not self.match('ID'):
            self.error("Esperado identificador")
        ids.append(self.tokens[self.position - 1][1])
        while self.match('COMMA'):
            if not self.match('ID'):
                self.error("Esperado identificador após ','")
            ids.append(self.tokens[self.position - 1][1])
        return ids

    # Função para blocos de comandos
    def bloco(self):
        while self.tokens[self.position][0] in ['READ', 'WRITE', 'ID', 'IF', 'WHILE', 'FOR']:
            self.cmd()

    def cmd(self):
        if self.match('READ'):
            self.cmd_leitura()
        elif self.match('WRITE'):
            self.cmd_escrita()
        elif self.match('IF'):
            self.cmd_if()
        elif self.match('WHILE'):
            self.cmd_while()
        elif self.match('FOR'):  # Aqui estamos reconhecendo 'paraCada'
            self.cmd_para()
        elif self.tokens[self.position][0] == 'ID' and self.tokens[self.position + 1][0] == 'ASSIGN':
            self.cmd_expr()
        else:
            self.error("Comando inválido")


    def cmd_leitura(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'ler'")
        if not self.match('ID'):
            self.error("Esperado identificador em 'ler'")
        var_name = self.tokens[self.position - 1][1]
        self.semantic_analyzer.check_variable(var_name)  # Verifica se a variável foi declarada
        if not self.match('RPAREN'):
            self.error("Esperado ')' após identificador em 'ler'")
        if not self.match('DOT'):
            self.error("Esperado '.' após comando 'ler'")
        self.generator.add_line(f"{var_name} = input()")

    def cmd_escrita(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'escreva'")
        if self.match('STRING'):
            text = self.tokens[self.position - 1][1]
            self.generator.add_line(f"print({text})")
        elif self.match('ID'):
            var_name = self.tokens[self.position - 1][1]
            self.semantic_analyzer.check_variable(var_name)  # Verifica se a variável foi declarada
            self.generator.add_line(f"print({var_name})")
        else:
            self.error("Esperado string ou identificador em 'escreva'")
        if not self.match('RPAREN'):
            self.error("Esperado ')' após 'escreva'")
        if not self.match('DOT'):
            self.error("Esperado '.' após comando 'escreva'")

    def parse_operador_relacional(self, operador):
        operadores_map = {
            'menor': '<',
            'maior': '>',
            'igual': '==',
            'diferente': '!=',
            'menor_igual': '<=',
            'maior_igual': '>='
        }
        return operadores_map.get(operador, operador)

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

    def cmd_expr(self):
        if not self.match('ID'):
            self.error("Esperado identificador")
        var_name = self.tokens[self.position - 1][1]
        if not self.match('ASSIGN'):
            self.error("Esperado 'recebe' para atribuição")
        expression_code = self.expr()
        expression_type = self.semantic_analyzer.check_variable(var_name)
        self.semantic_analyzer.check_type_compatibility(var_name, expression_type)  # Verifica compatibilidade de tipos
        if not self.match('DOT'):
            self.error("Esperado '.' após atribuição")
        self.generator.add_line(f"{var_name} = {expression_code}")

    def parse_operador_matematico(self, operador):
        operadores_map = {
            'mais': '+',
            'menos': '-',
            'vezes': '*',
            'dividido': '/'
        }
        return operadores_map.get(operador, operador)

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

    def fator(self):
        if self.match('NUMBER'):
            code = self.tokens[self.position - 1][1]
            return code, "inteiro" if '.' not in code else "decimal"
        elif self.match('ID'):
            var_name = self.tokens[self.position - 1][1]
            var_type = self.semantic_analyzer.check_variable(var_name)
            return var_name, var_type
        elif self.match('LPAREN'):
            code, expr_type = self.expr()
            if not self.match('RPAREN'):
                self.error("Esperado ')' após expressão")
            return f"({code})", expr_type
        else:
            self.error("Fator esperado")
        
    def cmd_para(self):
        if not self.match('FOR'):
            self.error("Esperado 'paraCada'")

        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'paraCada'")

        # Inicialização: i recebe 0
        init_code = self.cmd_expr(for_loop=True)  # O primeiro comando de atribuição (inicialização)
        
        if not self.match('SEMI'):
            self.error("Esperado ';' após inicialização em 'paraCada'")

        # Condição: i menor 10
        condition = self.expr()  # Expressão que define a condição do loop
        
        if not self.match('SEMI'):
            self.error("Esperado ';' após condição em 'paraCada'")

        # Incremento: i recebe i mais 1
        increment_code = self.cmd_expr(for_loop=True)  # Comando de incremento
        
        if not self.match('RPAREN'):
            self.error("Esperado ')' após incremento em 'paraCada'")

        if not self.match('LBRACE'):
            self.error("Esperado '{' após 'paraCada'")

        # Adiciona o código do loop em Python
        self.generator.add_line(f"{init_code}  # Inicialização")
        self.generator.add_line(f"for {increment_code}:")  # Traduzido para o formato de um 'for' em Python
        self.generator.increase_indent()
        self.bloco()  # Processa o bloco de código dentro do 'for'
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'paraCada'")

