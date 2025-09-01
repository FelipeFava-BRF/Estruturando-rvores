import heapq
from typing import List, Tuple, Set, Dict, Optional
from collections import deque

Coord = Tuple[int, int]

# =========================
# Utilitários base do usuário
# =========================

def manhattan_distance(pos1: Coord, pos2: Coord) -> int:
    """Calcula a distância de Manhattan entre dois pontos."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def print_grid(grid: List[List[int]], path: List[Coord], start: Coord, goal: Coord, current: Coord = None):
    """Imprime o grid com caminho parcial, início, objetivo e posição atual (opcional)."""
    display = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # Marca obstáculos com '#'
    for x, y in [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 1]:
        display[x][y] = '#'
    # Marca o caminho com '*'
    for x, y in path:
        display[x][y] = '*'
    # Marca o ponto inicial e objetivo
    display[start[0]][start[1]] = 'S'
    display[goal[0]][goal[1]] = 'G'
    # Marca a posição atual
    if current and current != start and current != goal:
        display[current[0]][current[1]] = 'C'
    for row in display:
        print(' '.join(row))

# =========================
# Planta-baixa por cômodos
# =========================

def build_house_grid() -> Tuple[
    List[List[int]],
    Dict[str, Set[Coord]],
    Dict[Coord, Optional[str]],
    Set[frozenset]
]:
    """
    Constrói uma planta 8x8 com cômodos (A..G).
    - grid: 0 = livre (dentro de cômodos), 1 = parede/fora
    - rooms: letras -> conjunto de coordenadas
    - cell_to_room: célula -> letra do cômodo (ou None se não pertence)
    - door_edges: pares de células adjacentes que cruzam de um cômodo a outro (portas)
    """
    rows, cols = 8, 8
    grid = [[1 for _ in range(cols)] for _ in range(rows)]  # tudo parede inicialmente

    # Cômodos com formatos variados (conforme exemplo anterior)
    rooms: Dict[str, Set[Coord]] = {
        "A": {(0,0), (0,1), (1,0), (1,1)},                    # 2x2
        "B": {(0,2), (1,2), (2,2)},                           # 3x1 (vertical)
        "C": {(0,3), (0,4), (1,3), (1,4)},                    # 2x2
        "D": {(3,0), (3,1), (3,2), (3,3)},                    # 1x4 (horizontal)
        "E": {(2,4), (3,4), (3,5), (4,5)},                    # formato L
        "F": {(4,1), (5,1)},                                  # 2x1 (vertical)
        "G": {(5,5), (5,6), (5,7)},                           # 1x3 (horizontal)
    }

    # Marca células dos cômodos como livres (0)
    for cells in rooms.values():
        for (i, j) in cells:
            grid[i][j] = 0

    # Mapeamento célula -> cômodo
    cell_to_room: Dict[Coord, Optional[str]] = {}
    for rname, cells in rooms.items():
        for c in cells:
            cell_to_room[c] = rname
    # Células não pertencentes a cômodos ficam como None
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in cell_to_room:
                cell_to_room[(i, j)] = None

    # Portas: qualquer adjacência (4-vizinhança) entre células de cômodos distintos
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    door_edges: Set[frozenset] = set()
    for (i, j), r1 in cell_to_room.items():
        if r1 is None:
            continue
        for di, dj in directions:
            ni, nj = i+di, j+dj
            if 0 <= ni < rows and 0 <= nj < cols:
                r2 = cell_to_room[(ni, nj)]
                if r2 is not None and r2 != r1:
                    door_edges.add(frozenset({(i, j), (ni, nj)}))

    return grid, rooms, cell_to_room, door_edges

def room_anchor(rooms: Dict[str, Set[Coord]], r: str) -> Coord:
    """Escolhe uma célula âncora 'estável' de um cômodo (menor coordenada)."""
    return sorted(list(rooms[r]))[0]

# =========================
# Buscas no GRID (4-vizinhos)
# =========================

def reconstruct_path(came_from: Dict[Coord, Optional[Coord]], current: Coord) -> List[Coord]:
    path: List[Coord] = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]

def greedy_search(grid: List[List[int]], start: Coord, goal: Coord) -> List[Coord]:
    """
    Busca Gulosa Best-First usando Manhattan. Imprime frontier/visited/tabuleiro a cada iteração
    (mantido conforme sua base).
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    frontier: List[Tuple[int, Coord]] = [(manhattan_distance(start, goal), start)]
    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    visited: Set[Coord] = set()
    iteration = 0

    while frontier:
        iteration += 1
        print(f"\n--- Iteração {iteration} (Greedy) ---")
        print("Frontier (distância de Manhattan, posição):", [(dist, pos) for dist, pos in frontier])
        print("Visited:", sorted(list(visited)))

        _, current = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        # caminho parcial até o atual (para visualização)
        partial_path = reconstruct_path(came_from, current)
        print("Tabuleiro (S=início, G=obj, #=obst, .=livre, C=atual, *=caminho):")
        print_grid(grid, partial_path, start, goal, current)

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                nxt = (nx, ny)
                if nxt not in visited:
                    heapq.heappush(frontier, (manhattan_distance(nxt, goal), nxt))
                    if nxt not in came_from:
                        came_from[nxt] = current

    return []

def bfs_search(grid: List[List[int]], start: Coord, goal: Coord) -> List[Coord]:
    """Busca em Largura (ótima em menor nº de passos/células)."""
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    q = deque([start])
    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    visited: Set[Coord] = {start}

    while q:
        u = q.popleft()
        if u == goal:
            return reconstruct_path(came_from, u)
        for dx, dy in directions:
            nx, ny = u[0]+dx, u[1]+dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                v = (nx, ny)
                if v not in visited:
                    visited.add(v)
                    came_from[v] = u
                    q.append(v)
    return []

def dfs_search(grid: List[List[int]], start: Coord, goal: Coord) -> List[Coord]:
    """Busca em Profundidade (não garante ótimo)."""
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    stack = [start]
    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    visited: Set[Coord] = {start}

    while stack:
        u = stack.pop()
        if u == goal:
            return reconstruct_path(came_from, u)
        for dx, dy in directions:
            nx, ny = u[0]+dx, u[1]+dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                v = (nx, ny)
                if v not in visited:
                    visited.add(v)
                    came_from[v] = u
                    stack.append(v)
    return []

# =========================
# Métricas e comparação
# =========================

def count_door_crossings(path: List[Coord], cell_to_room: Dict[Coord, Optional[str]]) -> int:
    """
    Conta quantas vezes o caminho entra em um novo cômodo (ignorando movimentos internos).
    Cada mudança de cômodo = 1 cruzamento de porta.
    """
    if not path:
        return 0
    crossings = 0
    last_room: Optional[str] = cell_to_room.get(path[0])
    for c in path[1:]:
        r = cell_to_room.get(c)
        if r is not None and r != last_room and last_room is not None:
            crossings += 1
        if r is not None:
            last_room = r  # atualiza quando estiver efetivamente em um cômodo
    return crossings

def summarize(name: str, path: List[Coord], cell_to_room: Dict[Coord, Optional[str]], time_per_door: float):
    if not path:
        print(f"{name}: sem caminho.\n")
        return
    doors = count_door_crossings(path, cell_to_room)
    total_time = doors * time_per_door
    print(f"{name}:")
    print(f"  - Tamanho do caminho (células): {len(path)}")
    print(f"  - Portas cruzadas: {doors}")
    print(f"  - Tempo total (s): {total_time:.2f}")
    print(f"  - Caminho: {path}\n")

# =========================
# Execução
# =========================

def main():
    # Constrói a planta
    grid, rooms, cell_to_room, door_edges = build_house_grid()

    # Exibe visão geral da planta (sem caminho)
    print("Grid inicial (S = início, G = objetivo, # = obstáculo, . = livre):")
    # Para exibir, precisamos de start/goal fictícios (só para visual). Usaremos âncoras de A e G
    start_r, goal_r = "A", "G"
    start = room_anchor(rooms, start_r)
    goal = room_anchor(rooms, goal_r)
    print_grid(grid, [], start, goal)

    print("\nCômodos e tamanhos:")
    for r in sorted(rooms.keys()):
        print(f"  {r}: {len(rooms[r])} células")
    print("\nPortas (adjacências entre cômodos diferentes):", len(door_edges))

    # Você pode escolher origem/destino por CÔMODO (letras) ou por COORDENADAS.
    # a) Por cômodo:
    start_room = "A"
    goal_room  = "G"
    start = room_anchor(rooms, start_room)
    goal  = room_anchor(rooms, goal_room)

    # b) Alternativamente, por coordenadas (descomente e ajuste):
    # start = (0, 0)  # dentro de A
    # goal  = (5, 7)  # dentro de G

    time_per_door = 5.0  # segundos por porta
    print(f"\nOrigem (cômodo): {start_room} -> célula {start}")
    print(f"Destino (cômodo): {goal_room} -> célula {goal}")
    print(f"Tempo por porta: {time_per_door}s\n")

    # Executa buscas
    path_greedy = greedy_search(grid, start, goal)
    path_bfs    = bfs_search(grid, start, goal)
    path_dfs    = dfs_search(grid, start, goal)

    # Sumário e comparação
    print("\n--- Comparação de Caminhos ---")
    summarize("Gulosa", path_greedy, cell_to_room, time_per_door)
    summarize("BFS   ", path_bfs,    cell_to_room, time_per_door)
    summarize("DFS   ", path_dfs,    cell_to_room, time_per_door)

if __name__ == "__main__":
    main()
