#Progressão para entender árvores - listas ligadas (encadeadas) + pilhas + filas -> árvores binárias -> árvores n-árias -> grafos é uma progressão bastante lógica.

from collections import deque

class No:
    def __init__ (self, info):
        self.info = info
        self.filhos = []


def printArvore(no, nivel=0, prefixo="Raiz", visitados=None):
    if visitados is None:
        visitados = set()

    if no is None or no.info in visitados:
        return

    visitados.add(no.info)
    print("   " * nivel + f"{prefixo} └── {no.info}")
    for i, filho in enumerate(no.filhos):
        novo_prefixo = "\\" if i % 2 == 0 else "-"
        printArvore(filho, nivel + 1, novo_prefixo, visitados)
    
    
def construirArvoreInterativa():
    nome_para_no = {}
    cidades_processadas = set()

    origem = input("Digite a cidade de origem (raiz da árvore): ").strip()
    destino = input("Digite a cidade de destino: ").strip()

    raiz = No(origem)
    nome_para_no[origem] = raiz
    fila = [raiz]

    while fila:
        atual = fila.pop(0)

        if atual.info in cidades_processadas:
            continue #já processamos os vizinhos dessa cidade

        vizinhos = input(f"Digite as cidades vizinhas de {atual.info} (mínimo 1, separados por vírgula): ")

        if vizinhos.lower() == "fim" or vizinhos == "":
            cidades_processadas.add(atual.info)
            continue #pula para o próximo nó na fila

        nomes = [nome.strip() for nome in vizinhos.split(",") if nome.strip()]
        if len(nomes) < 1:
            print("Precisa informar pelo menos 1 cidade vizinha ou digitar 'fim'.")
            fila.append(atual)
            continue
            
        for nome in nomes:
            if nome in nome_para_no:
                novo_no = nome_para_no[nome]
            else:

                novo_no = No(nome)
                nome_para_no[nome] = novo_no
                fila.append(novo_no)
            
            atual.filhos.append(novo_no)

            if nome == destino:
                print(f"\nCidade de destino '{destino}' encontrada!")
                continuar = input("Deseja continuar adicionando vizinhos? (s/n): ").strip()
                if continuar != "s":
                    tipo_busca = input("Deseja buscar o caminho usando:\n1 - Busca em Largura \n2 - Busca em Profundidade \n3- Ambas \nEscolha: ")

                    match(tipo_busca):
                        case"1":
                            caminhos = buscarLargura(raiz, destino)
                        case"2":
                            caminhos = buscarProfundidade(raiz, destino)
                        case"3":
                            caminhos = buscarLargura(raiz, destino) + buscarProfundidade(raiz, destino)
                        case _:
                            print("Escolha uma opção de 1 a 3")
                    
                    if caminhos:
                        print(f"Caminhos encontrados de {raiz.info} até {destino} ({tipo_busca}):")
                        for i, caminho in enumerate(caminhos, 1):
                            print(f"  Caminho {i}: {' -> '.join(caminho)}")
                    else:
                        print(f"\nNenhum caminho encontrado de {raiz.info} até {destino}.")

        cidades_processadas.add(atual.info)
        
        print("\nÁrvore atualizada:")
        printArvore(raiz)
        print("-" * 40)

    return raiz, destino

def buscarProfundidade(raiz, destino):
    caminhos = []

    def dfs(no, caminho):
        if no is None:
            return
        caminho.append(no.info)
        if no.info == destino:
            caminhos.append(list(caminho))
        else:
            for filho in no.filhos:
                dfs(filho, caminho)
        caminho.pop()

    dfs(raiz, [])
    return caminhos


def buscarLargura(raiz, destino):
    caminhos = []
    fila = deque([(raiz, [raiz.info])])

    while fila:
        atual, caminho = fila.popleft()

        if atual.info == destino:
            caminhos.append(caminho)
        
        for filho in atual.filhos:
            fila.append((filho, caminho + [filho.info]))

    return caminhos


if __name__ == "__main__":
    raiz, destino = construirArvoreInterativa()
    print("\n Árvore Final Construída:")
    printArvore(raiz)

    
