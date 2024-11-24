from lexer import tokenize

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
        self.position = 0  # Inicializa a posição atual no fluxo de tokens
        self.generator = CodeGenerator()
        self.semantic_analyzer = SemanticAnalyzer()

    def parse_operador_relacional(self, operador):
        operadores_map = {
        'menor': '<',
        'maior': '>',
        'igual': '==',
        'diferente': '!=',
        'menor_igual': '<=',
        'maior_igual': '>=',
        'modulo': '%',  # Adicionado
    }
        if operador not in operadores_map:
            raise ValueError(f"Erro Semântico: Operador relacional '{operador}' inválido.")
        return operadores_map[operador]


    def match(self, expected_type):
        """Verifica se o token atual corresponde ao tipo esperado."""
        if self.position < len(self.tokens) and self.tokens[self.position][0] == expected_type:
           self.position += 1  # Avança para o próximo token
           return True
        return False

    def cmd_if(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'dadoQue'")

        # Processa o lado esquerdo da condição
        left_expr, left_type = self.expr()

        if not self.match('REL_OP'):
            self.error("Operador relacional esperado em 'dadoQue'")
        operador = self.tokens[self.position - 1][1]
        operador_python = self.parse_operador_relacional(operador)

        # Processa o lado direito da condição
        right_expr, right_type = self.expr()

        if not self.match('RPAREN'):
            self.error("Esperado ')' após expressão em 'dadoQue'")

        # Gera o código para a condicional
        self.generator.add_line(f"if {left_expr} {operador_python} {right_expr}:")
        self.generator.increase_indent()

        if not self.match('LBRACE'):
            self.error("Esperado '{' após condição 'dadoQue'")
        self.bloco()
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'dadoQue'")


    def error(self, message="Erro de Sintaxe"):
        current_token = self.tokens[self.position] if self.position < len(self.tokens) else "EOF"
        raise SyntaxError(f"{message} no token {current_token} na posição {self.position}")

    def parse(self):
        self.program()
        return self.generator.get_code()

    def program(self):
        if not self.match('PROGRAM'):
            self.error("Esperado 'inicioDoPrograma'")
        self.declara()
        self.bloco()
        if not self.match('END_PROGRAM'):
            self.error("Esperado 'fimDoPrograma'")

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
            if not self.match('TERMINATOR'):
                self.error("Esperado '|' após declaração")

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
            self.cmd_while()  # Adiciona suporte ao comando 'enquanto'
        elif self.match('FOR'):
            self.cmd_para()
        elif self.tokens[self.position][0] == 'ID' and self.tokens[self.position + 1][0] == 'ASSIGN':
            self.cmd_expr()
        else:
            self.error("Comando inválido")

    def cmd_while(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'enquanto'")

        # Processa o lado esquerdo da condição
        left_expr, left_type = self.expr()

        if not self.match('REL_OP'):
            self.error("Operador relacional esperado em 'enquanto'")
        operador = self.tokens[self.position - 1][1]
        operador_python = self.parse_operador_relacional(operador)

        # Processa o lado direito da condição
        right_expr, right_type = self.expr()

        if not self.match('RPAREN'):
            self.error("Esperado ')' após expressão em 'enquanto'")

        # Gera o código para o laço enquanto
        self.generator.add_line(f"while {left_expr} {operador_python} {right_expr}:")
        self.generator.increase_indent()

        if not self.match('LBRACE'):
            self.error("Esperado '{' após condição 'enquanto'")
        self.bloco()
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'enquanto'")


    def cmd_leitura(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'leia'")
        if not self.match('ID'):
            self.error("Esperado identificador em 'leia'")
        var_name = self.tokens[self.position - 1][1]
        var_type = self.semantic_analyzer.check_variable(var_name)  # Obtém o tipo esperado da variável
        if not self.match('RPAREN'):
            self.error("Esperado ')' após identificador em 'leia'")
        if not self.match('TERMINATOR'):
            self.error("Esperado '|' após comando 'leia'")
        # Converte com base no tipo esperado
        if var_type == "inteiro":
            self.generator.add_line(f"{var_name} = int(input())")
        elif var_type == "decimal":
            self.generator.add_line(f"{var_name} = float(input())")
        elif var_type == "texto":
            self.generator.add_line(f"{var_name} = input()")

    def cmd_escrita(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'escreva'")
        if self.match('STRING'):
            text = self.tokens[self.position - 1][1]
            self.generator.add_line(f"print({text})")
        elif self.match('ID'):
            var_name = self.tokens[self.position - 1][1]
            self.semantic_analyzer.check_variable(var_name)
            self.generator.add_line(f"print({var_name})")
        else:
            self.error("Esperado string ou identificador em 'escreva'")
        if not self.match('RPAREN'):
            self.error("Esperado ')' após 'escreva'")
        if not self.match('TERMINATOR'):
            self.error("Esperado '|' após comando 'escreva'")

    def cmd_expr(self):
        if not self.match('ID'):
            self.error("Esperado identificador")
        var_name = self.tokens[self.position - 1][1]
        if not self.match('ASSIGN'):
            self.error("Esperado 'recebe' para atribuição")
        expression_code, expression_type = self.expr()  # Retorna o código da expressão e o tipo
        var_type = self.semantic_analyzer.check_variable(var_name)  # Tipo esperado para a variável
        self.semantic_analyzer.check_type_compatibility(var_name, expression_type)  # Verifica compatibilidade
        if not self.match('TERMINATOR'):
            self.error("Esperado '|' após atribuição")
        self.generator.add_line(f"{var_name} = {expression_code}")  # Adiciona o código da atribuição



    def expr(self):
        left_code, left_type = self.termo()
        while self.match('ADD_OP'):
            op = self.tokens[self.position - 1][1]
            op_python = {'mais': '+', 'menos': '-'}.get(op, op)
            right_code, right_type = self.termo()
            left_code = f"({left_code} {op_python} {right_code})"
            left_type = "decimal" if left_type == "decimal" or right_type == "decimal" else "inteiro"
        return left_code, left_type



    def termo(self):
        left_code, left_type = self.fator()
        while self.match('MUL_OP') or self.match('MOD_OP'):  # Inclui MOD_OP
            op = self.tokens[self.position - 1][1]
            op_python = {'vezes': '*', 'dividido': '/', 'modulo': '%'}.get(op, op)
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
        elif self.match('STRING'):  # Novo suporte para strings
           string_value = self.tokens[self.position - 1][1]
           return string_value, "texto"
        elif self.match('LPAREN'):
           code, expr_type = self.expr()
           if not self.match('RPAREN'):
               self.error("Esperado ')' após expressão")
           return f"({code})", expr_type
        else:
           self.error("Fator esperado")


