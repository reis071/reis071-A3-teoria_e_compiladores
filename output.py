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