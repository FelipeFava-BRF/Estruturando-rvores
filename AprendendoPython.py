
# print(1.0**1.0)
# print("\n")
# print(2**1) #2¹ = 2
# print("\n")
# print(2**2) #2² = 4

# print(2 // 2) #1
# print("\n")
# print(2 / 3) #resto 0,667
# print("\n")
# print(2 // 3) #aproxima o denominador para 0

# print("\nLaço For")
# for i in range(10):
#     print("Número: ", i)

# print("\nLaço While")

# contador = 0
# while contador < 5:
#     print("Contador: ", contador)
#     contador += 1 # o mesmo que contador = contador + 1

#Calculadora Simples

# continuar = True

# while continuar:
#     numero1 = float(input("Digite o primeiro número: "))

#     numero2 = float(input("Digite o segundo número: "))
    
#     print(f"\nSoma: {numero1 + numero2}")

#     print(f"\nSubtração: {numero1 - numero2}")

#     print(f"\nMultiplicação: {numero1 * numero2}")

#     print(f"\nDivisão (resto): {numero1 / numero2}")

#     print(f"\nDivisão (denominador): {numero1 // numero2}")

#     continuar = input("Continuar a digitar? (s/n): ").lower()

#     if continuar == "n":
#         print("Acabou")
#         continuar = False


# def media(param1, param2, param3):

#     media = (param1 + param2 + param3) / 3
#     return media #posso também retornar a função direto - return (param1 + param2 + param3) / 3

# param1  = float(input("Informe o primeiro valor: "))
# param2 = float(input("Informe o segundo valor: "))
# param3 = float(input("Informe o terceiro valor: "))
    
# resultado = media(param1, param2, param3)

# print(f"A média dos valores são: {resultado:.2f}") # :.2f expressa que queremos apenas duas casas após a vírgula

#Listas - sequências ordenadas e mutáveis
frutas = ["uva", "maçã", "banana"]
frutas.append("limão")
print(frutas)
frutas.append("abacaxi")
print(frutas[4])

#Dicionários - pares chave - valor
aluno = {
    "nome": "João",
    "idade": 24
    }

# print(aluno) - não funciona
# print(aluno["nome"])
# print(aluno["idade"])

livro1 = {
    "nome": "as aventuras de pi",
    "ano publicacao": "2001",
    "escritor": "Yann Martel"
}

print(livro1["nome"])
print(livro1["ano publicacao"])
print(livro1["escritor"])


#Tuplas - sequências ordenadas e imutáveis
coordenadas = (20, 15)

#Conjuntos - Coleções não ordenadas e sem elementos duplicados.
numeros = {1, 2, 3, 3, 2}
print(numeros) # {1, 2, 3}

# Use o módulo random para gerar um número aleatório entre 1 e 100.
# Projeto Prático: Mini Sistema de Cadastro
# Crie um programa que:

# Usa funções para cadastrar usuários.
# Armazena os dados em uma lista de dicionários.
# Exibe todos os usuários cadastrados.