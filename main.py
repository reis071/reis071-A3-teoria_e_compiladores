import sys
from lexer import tokenize
from parser import Parser

def read_code(file_path):
    """Lê o código do arquivo fornecido pelo usuário."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def compile_to_python(code):
    """Compila o código da linguagem fictícia para Python."""
    tokens = tokenize(code)  # Tokeniza o código
    parser = Parser(tokens)  # Cria o parser com os tokens
    return parser.parse()  # Retorna o código Python gerado

def save_and_run(generated_code, output_file='output.py'):
    """Salva o código Python gerado e o executa."""
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
