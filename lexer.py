import re

tokens_definitions = {
    'PROGRAM': r'\binicioDoPrograma\b',
    'END_PROGRAM': r'\bfimDoPrograma\b',
    'INT': r'\binteiro\b',
    'DECIMAL': r'\bdecimal\b',
    'TEXT': r'\btexto\b',
    'BOOLEAN': r'\bbooleano\b',
    'TRUE': r'\bverdadeiro\b',
    'FALSE': r'\bfalso\b',
    'IF': r'\bdadoQue\b',
    'ELSE': r'\bsenao\b',
    'WHILE': r'\benquanto\b',
    'FOR': r'\bparaCada\b',
    'READ': r'\bleia\b',
    'WRITE': r'\bescreva\b',
    'ASSIGN': r'recebe',
    'REL_OP': r'menor_igual|maior_igual|igual|diferente|menor|maior',  # Ajustado
    'ADD_OP': r'mais|menos',
    'MUL_OP': r'vezes|dividido',
    'MUL_OP': r'vezes|dividido',
    'MOD_OP': r'modulo', 
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'COMMA': r',',
    'SEMI': r';',
    'TERMINATOR': r'\|',
    'NUMBER': r'\d+(\.\d+)?',
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING': r'"[^"]*"',
    'NEWLINE': r'\n',
    'WHITESPACE': r'[ \t]+',
}

# Função para o Lexer
def lex(code):
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
            raise SyntaxError(f'Erro Léxico: caractere inesperado "{code[position]}" na posição {position}')
    return tokens_found

# Função para gerar tokens de um código de entrada
def tokenize(code):
    return lex(code)

def test_rel_op():
    test_code = "menor_igual maior_igual igual diferente menor maior"
    try:
        tokens = tokenize(test_code)
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    test_rel_op()
