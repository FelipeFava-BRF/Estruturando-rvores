
# o desafio consiste numa planta-baixa de uma casa com diferentes cômodos/quartos. Você precisa fazer um código para o robô aspirador que irá navegar por esses cômodos.
# cada cômodo pode possuir 1 ou mais portas que dão acesso a outros cômodos, todos os cômodos possuem 4 paredes e todos os cômodos são acessíveis (possuem pelo menos uma porta).
# o robô precisa saber o melhor / menor caminho usando algoritmos de busca, como: busca em largura, busca em profundidade e busca gulosa.
# se o robô se locomover no mesmo cômodo não irá ser decrescentado nada e a distância será 0, mas se o robô passar alguma porta para ir a outro cômodo, terá um custo envolvido de locomoção do robô.
# represente usando matriz a planta-baixa dessa casa, com você definindo qual o tamanho dos cômodos, a localização das paredes e das portas pelas coordenadas dadas a matriz. Exemplo: A tem tamanho de 4, 2x2
# Exemplo: A tem tamanho de 4, 2x2 (2 linhas e 2 colunas), coordenadas (0, 0), (0, 1), (1, 0) e (1, 1) é uma estrutura quadrada. Mas nem todos os cômodos são quadrados, uns são em formato de tiras (linhas ou colunas).
# Exemplo: B tem tamanho de 3, 3x1 (3 linhas e 1 coluna), coordenadas (2, 0), (3, 0), (4, 0) é uma estrutura reta na vertical.
# calcule o tempo que o robô leva para realizar um caminho definido pelo usuário em cada algoritmo de busca e compare os caminhos feitos.
# use a distância de Manhattan para calcular a menor distância que o robô deverá percorrer na matriz, isso é, ir do ponto X ao ponto Y da casa.

from collections import deque
import heapq

# -----------------------
# Planta-baixa (8 x 8)
# -----------------------
# Representação:
# - Cada cômodo é um conjunto de células (linha, coluna)
# - Portas são pares de células adjacentes (4-vizinhança) que pertencem a cômodos diferentes
# - Grafo: vértices = cômodos; arestas = portas (custo unitário por porta)

def build_house():
    # Define cômodos com formatos variados
    rooms = {
        # A: 2x2 (quadrado)
        "A": {(0,0), (0,1), (1,0), (1,1)},
        # B: 3x1 (tira vertical na coluna 2)
        "B": {(0,2), (1,2), (2,2)},
        # C: 2x2 (bloco à direita de B)
        "C": {(0,3), (0,4), (1,3), (1,4)},
        # D: 1x4 (tira horizontal)
        "D": {(3,0), (3,1), (3,2), (3,3)},
        # E: formato L
        "E": {(2,4), (3,4), (3,5), (4,5)},
        # F: 2x1 (tira vertical)
        "F": {(4,1), (5,1)},
        # G: 1x3 (tira horizontal)
        "G": {(5,5), (5,6), (5,7)},
    }

    # Portas entre cômodos (pares de células adjacentes)
    doors = [
        # A <-> B
        ((0,1), (0,2), "A", "B"),
        # B <-> C
        ((1,2), (1,3), "B", "C"),
        # B <-> D
        ((2,2), (3,2), "B", "D"),
        # C <-> E
        ((1,4), (2,4), "C", "E"),
        # D <-> F
        ((3,1), (4,1), "D", "F"),
        # E <-> G
        ((4,5), (5,5), "E", "G"),
    ]

    # Matriz para visualização
    rows, cols = 8, 8
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for rname, cells in rooms.items():
        for (i, j) in cells:
            grid[i][j] = rname

    # Grafo de conexões entre cômodos a partir das portas
    graph = {r: set() for r in rooms}
    for (_, _, ra, rb) in doors:
        graph[ra].add(rb)
        graph[rb].add(ra)

    return grid, rooms, doors, graph


def print_grid(grid):
    print("Planta (8x8) - '.' são paredes externas/área fora de cômodos:")
    for row in grid:
        print(" ".join(row))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def room_manhattan(rooms, r1, r2):
    """Menor distância Manhattan entre quaisquer células dos cômodos r1 e r2."""
    best = float("inf")
    for c1 in rooms[r1]:
        for c2 in rooms[r2]:
            d = manhattan(c1, c2)
            if d < best:
                best = d
    return best


# -----------------------
# Algoritmos de busca em nível de CÔMODO
# -----------------------

def bfs(graph, start, goal):
    """Busca em Largura (ótima em # de portas quando todas têm mesmo custo)."""
    q = deque([start])
    visited = {start}
    parent = {start: None}
    while q:
        u = q.popleft()
        if u == goal:
            break
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                q.append(v)
    if goal not in parent:
        return None
    # Reconstrói caminho
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def dfs(graph, start, goal):
    """Busca em Profundidade (não garante caminho ótimo)."""
    stack = [start]
    visited = {start}
    parent = {start: None}
    while stack:
        u = stack.pop()
        if u == goal:
            break
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                stack.append(v)
    if goal not in parent:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def greedy_best_first(graph, rooms, start, goal):
    """Busca Gulosa (Best-First) com heurística Manhattan entre cômodos."""
    h = lambda r: room_manhattan(rooms, r, goal)
    pq = [(h(start), start)]
    visited = {start}
    parent = {start: None}
    while pq:
        _, u = heapq.heappop(pq)
        if u == goal:
            break
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                heapq.heappush(pq, (h(v), v))
    if goal not in parent:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def path_time(path, time_per_door=5.0):
    """Tempo total considerando custo 0 dentro do cômodo e custo fixo por porta."""
    if not path or len(path) < 2:
        return 0.0
    doors = len(path) - 1
    return doors * time_per_door


# -----------------------
# Demonstração
# -----------------------
if __name__ == "__main__":
    grid, rooms, doors, graph = build_house()
    print_grid(grid)
    print("\nPortas (pares de células):")
    for (c1, c2, r1, r2) in doors:
        print(f"  {r1} {c1} <-> {r2} {c2}")

    start, goal = "A", "G"
    time_per_door = 5.0

    print(f"\nOrigem: {start}, Destino: {goal}")
    print("Distância Manhattan mínima entre cômodos:", room_manhattan(rooms, start, goal))

    pbfs = bfs(graph, start, goal)
    pdfs = dfs(graph, start, goal)
    pgreedy = greedy_best_first(graph, rooms, start, goal)

    print("\nCaminhos:")
    print("BFS   :", pbfs, "| portas:", len(pbfs)-1 if pbfs else None, "| tempo:", path_time(pbfs, time_per_door))
    print("DFS   :", pdfs, "| portas:", len(pdfs)-1 if pdfs else None, "| tempo:", path_time(pdfs, time_per_door))
    print("Gulosa:", pgreedy, "| portas:", len(pgreedy)-1 if pgreedy else None, "| tempo:", path_time(pgreedy, time_per_door))
