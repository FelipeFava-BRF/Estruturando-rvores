
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
# frutas = ["uva", "maçã", "banana"]
# frutas.append("limão")
# print(frutas)
# frutas.append("abacaxi")
# print(frutas[4])

# #Dicionários - pares chave - valor
# aluno = {
#     "nome": "João",
#     "idade": 24
#     }

# # print(aluno) - não funciona
# # print(aluno["nome"])
# # print(aluno["idade"])

# livro1 = {
#     "nome": "as aventuras de pi",
#     "ano publicacao": "2001",
#     "escritor": "Yann Martel"
# }

# print(livro1["nome"])
# print(livro1["ano publicacao"])
# print(livro1["escritor"])


# #Tuplas - sequências ordenadas e imutáveis
# coordenadas = (20, 15)

# #Conjuntos - Coleções não ordenadas e sem elementos duplicados.
# numeros = {1, 2, 3, 3, 2}
# print(numeros) # {1, 2, 3}

# Use o módulo random para gerar um número aleatório entre 1 e 100.

# import random as rd

# numero = rd.random() #numero float aleatorio
# print(numero)

# numero = rd.randbytes(1)
# print(numero)

# numero = rd.randint(1, 3) #gera um numero inteiro aleatorio dentro do intervalo definido
# print(numero)

# lista = range(100) #lista formada por um range de números de 0 a 100 -> range(0, 100)
# numero = rd.choice(lista) #numero float aleatorio escolhido da lista
# print(lista)
# print(numero)

# print("\nSortear Nova Lista\n")
# lista = ["maçã", "banana", "avestruz", "ovo", "leão", "raposa", "laranja"]
# novaLista = rd.sample(lista, 2) #sample retorna uma nova lista com n elementos formada a partir de uma primeira lista com n elementos
# print(novaLista)


# print("\nEmbaralhar lista\n")
# lista = ["maçã", "banana", "avestruz", "ovo", "leão", "raposa", "laranja"]
# novaLista = rd.shuffle(lista) #embaralha a lista existente
# print(novaLista) #retorna None por padrão
# print(lista) #retorna a lista de forma embaralhada

# print("\nGerar Seed\n")
# seed = rd.seed(50) #usado por trás dos outros geradores aleatórios
# print(rd.random()) #fixa um numero pseudoaleatorio

# Projeto Prático: Mini Sistema de Cadastro
# Crie um programa que:

# Usa funções para cadastrar usuários.
# Armazena os dados em uma lista de dicionários.
# Exibe todos os usuários cadastrados.

# def cadastrarFuncionarios(lista, id, nome, idade, salario):
#     #um dicionário
#     funcionario = {"id":id,
#                     "nome": nome,
#                    "idade": idade,
#                    "salario": salario}
#     lista.append(funcionario)
#     return lista

# funcionarios = [] #uma lista
# id_atual = 1 #começa com id 1

# try:
#     while True:
#         cadastrar = str(input("Cadastrar Funcionario? (s/n): ")).lower()

#         if cadastrar == "n":
#             print("\tCadastro Finalizado.")
#             break
        
#         nome = input("Digite o seu nome: ")
#         idade = int(input("Digite sua idade: "))
#         salario = float(input("Digite seu salário: "))
        
#         funcionarios = cadastrarFuncionarios(funcionarios, id_atual, nome, idade, salario)
#         id_atual += 1 #incrementa para o próxima funcionário

# except Exception as e:
#     print(f"\nErro encontrado: {e}")

# print("\nFuncionários Cadastrados:")
# for funcionario in funcionarios:
#     print(f"ID: {funcionario['id']}, Nome: {funcionario['nome']}, Idade: {funcionario['idade']}, Salário: R${funcionario['salario']:.2f}")    

#Projeto: Gerenciador de Tarefas (Simples)
# Objetivo:
# Criar um sistema que permite:
# Adicionar tarefas
# Listar tarefas
# Remover tarefas

# tarefas = []

# def adicionarTarefas(tarefa):
#     tarefas.append(tarefa)
#     print("Tarefa adicionada")

# def listarTarefas():
#     print("Tarefas: ")
#     for i, tarefa in enumerate(tarefas):
#         print(f"{i + 1}. {tarefa}")

# def excluirTarefas(indice):
#     if 0 <= indice < len(tarefas):
#         tarefas.pop(indice)
#         print("Tarefa removida")

# adicionarTarefas("Estudar")
# adicionarTarefas("Escutar")
# adicionarTarefas("Ler")
# listarTarefas()
# excluirTarefas(0) #comeca no indice 0
# listarTarefas()

# abre o arquivo dados.txt e escreve nele
# se o arquivo não foi criado, ele cria a partir do caminho em que você esteja executando o código
# *se executar o código no caminho da área de trabalho, o arquivo será criado na área de trabalho*
# se o arquivo já foi criado e escrito o texto, o comando não se repetirá, não criará um segundo arquivo e nem escreverá várias vezes a mesma coisa

# Escrevendo em um arquivo de texto
# with open("dados.txt", "w") as arquivo:
#     arquivo.write("Nome: Felipe\nIdade: 22")

# # Lendo o conteúdo do arquivo de texto
# with open("dados.txt", "r") as arquivo:
#     conteudo = arquivo.read()
#     print(conteudo)


# import csv # módulo para trabalhar com arquivos .csv

# Escrevendo no arquivo csv (separado por vírgulas)
# with open("usuarios.csv", "w", newline="") as arquivo:
#     escritor = csv.writer(arquivo)
#     escritor.writerow(["Nome", "Idade"])
#     escritor.writerow(["Felipe", 22])

# Lendo no arquivo csv
# with open("usuarios.csv", "r") as arquivo:
#     leitor = csv.reader(arquivo)
#     for linha in leitor:
#         print(linha)


# import json # biblioteca para trabalhar com json, basicamente a estrutura de dicionários com pares chave-valor -> {"chave": "valor"}

# # Escrevendo no arquivo json
# dados = {"nome": "Felipe", "idade": 22}
# with open("usuario.json", "w") as arquivo:
#     json.dump(dados, arquivo)

# # Lendo no arquivo json
# with open("usuario.json", "r") as arquivo:
#     dados_lidos = json.load(arquivo)
#     print(dados_lidos)

# def carregar_usuarios():
#     try:
#         with open("arquivo.json", "r") as arquivo:
#             return json.load(arquivo)
        
#     except FileNotFoundError:
#         return []

# def salvar_usuarios(usuarios):
#     with open("arquivo.json", "w") as arquivo:
#             json.dump(usuarios, arquivo, indent=4)

# def cadastrar_usuarios():
#     nome = input("Nome: ")
#     idade = int(input("Idade: "))
#     email = input("Email: ")
#     return {"nome": nome, "idade": idade, "email": email}

# def listar_usuarios(usuarios):
#     for usuario in usuarios:
#         print(f"{usuario['nome']} - {usuario['idade']} anos - {usuario['email']}")

# def main():
#     usuarios = carregar_usuarios()

#     while True:
#         print("\n1- Cadastrar \n2- Listar \n3- Sair")
#         opcao = input("Escolha: ")
#         if opcao == "1":
#             usuario = cadastrar_usuarios()
#             usuarios.append(usuario)
#             salvar_usuarios(usuarios)
#         elif opcao == "2":
#             listar_usuarios(usuarios)
#         elif opcao == "3":
#             break
#         else:
#             print("Opção Inválida")

# main()


import requests

# #método GET
# resposta1 = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
# print(resposta1.status_code) #status da resposta, número entre 100 e 599
# print("\n")
# dados = resposta1.json() #pegando toda a resposta e armazenando numa variavel
# print("Nome:", dados['name'], "\n", "Habilidades:", dados["abilities"]) #escolhendo o quero que apareça

# A PokeAPI não deixa fazer métodos que modifiquem a API, pois é para uso estático e público
#método POST
#irá retornar que não é possível fazer chamadas POST
# data = {'ability': ''}
# resposta = requests.post("https://pokeapi.co/api/v2/pokemon/ditto")
# print(resposta.text)

#Objetivo do projeto: Criar um script que consulta a previsão do tempo para uma cidade específica.

#Nesta você precisa ter uma conta nesse site do clima tempo para obter informações.
#De acordo, você pode fazer até 1000 chamadas por dia gratuitas.

def obter_previsao(cidade):
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': cidade,
        'appid': 'sua_chave_api',
        'lang': 'pt_br',
        'units': 'metric'
    }
    resposta2 = requests.get(url, params=params)
    if resposta2.status_code == 200:
        dados = resposta2.json()
        print(f"Clima em {cidade}: {dados['weather'][0]['description']}")
        print(f"Temperatura: {dados['main']['temp']}°C")
    else:
        print(f"Erro ao obter dados: {resposta2.status_code}")

obter_previsao('Itajaí')