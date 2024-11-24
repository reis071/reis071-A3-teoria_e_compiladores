numero = 0  # int
fatorial = 0  # int
contador = 0  # int
print("Digite um número para calcular o fatorial:")
numero = int(input())
fatorial = 1
contador = 1
while contador <= numero:
    fatorial = (fatorial * contador)
    contador = (contador + 1)
print("O fatorial de")
print(numero)
print("é:")
print(fatorial)