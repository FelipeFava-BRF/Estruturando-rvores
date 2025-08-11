#Progressão para entender árvores - listas ligadas (encadeadas) + pilhas + filas -> árvores binárias -> árvores n-árias -> grafos é uma progressão bastante lógica.

class No:
    def __init__ (self, info=None, esquerda=None, direita=None):
        self.info = info
        self.esquerda = esquerda
        self.direita = direita


def printArvore(no, nivel=0, lado="Raiz"):
    if no is None:
        return

    
    print("   " * nivel + f"{lado} └── {no.info}")
    printArvore(no.esquerda, nivel + 1, "Esq")
    printArvore(no.direita, nivel + 1, "Dir")

    


if __name__ == "__main__":

    "Criando nós manualmente"
    raiz = No("Arad")
    raiz.esquerda = No("Sibiu")
    raiz.direita = No("Timisoara")
    raiz.esquerda.esquerda = No("Fagaras")
    raiz.esquerda.direta = No("Rimnicu Vilcea")
    raiz.direita.direita = No("Lugoj")

    
    print("Impressão em profundidade (pré-ordem):")
    printArvore(raiz)

    # valor_no = {"Arad", "Bucarest", "Pitesti", "Oramed", "Crivoa", "Hirsovia", "Gurgiu"}
    # No = No(None, valor_no, valor_no, valor_no)
    # printArvore(No)
