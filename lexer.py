import re

# Definindo os tokens da linguagem
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
    'DOT': r'\|',  # Token para ponto final
    'NUMBER': r'\d+(\.\d+)?',
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING': r'"[^"]*"',  # Corrigido para permitir strings
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
            raise SyntaxError(f'Erro Léxico: caractere inesperado {code[position]} na posição {position}')
    return tokens_found

# Função para gerar tokens de um código de entrada
def tokenize(code):
    return lex(code)

# Função de teste
def test_lexer():
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

# Executar teste
if __name__ == "__main__":
    test_lexer()
