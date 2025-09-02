import heapq
import time
import csv
from typing import List, Tuple, Set, Dict, Optional
from collections import deque

Coordenada = Tuple[int, int]

# =========================
# Utilitários
# =========================

def distancia_manhattan(pos1: Coordenada, pos2: Coordenada) -> int:
    """Calcula a distância de Manhattan entre dois pontos."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def imprimir_grade(grade: List[List[int]], caminho: List[Coordenada],
                   inicio: Coordenada, objetivo: Coordenada, atual: Coordenada = None):
    """Imprime a grade com caminho parcial, início, objetivo e posição atual (opcional)."""
    exibicao = [['.' for _ in range(len(grade[0]))] for _ in range(len(grade))]
    # Obstaculos
    for x, y in [(i, j) for i in range(len(grade)) for j in range(len(grade[0])) if grade[i][j] == 1]:
        exibicao[x][y] = '#'
    # Caminho
    for x, y in caminho:
        exibicao[x][y] = '*'
    # Inicio e Objetivo
    exibicao[inicio[0]][inicio[1]] = 'S'
    exibicao[objetivo[0]][objetivo[1]] = 'G'
    # Atual
    if atual and atual != inicio and atual != objetivo:
        exibicao[atual[0]][atual[1]] = 'C'
    for linha in exibicao:
        print(' '.join(linha))

# =========================
# Planta-baixa por comodos
# =========================

def construir_grade_casa() -> Tuple[
    List[List[int]],
    Dict[str, Set[Coordenada]],
    Dict[Coordenada, Optional[str]],
    Set[frozenset]
]:
    """
    Constrói uma planta 8x8 com cômodos (A..G).
    - grade: 0 = livre (dentro de cômodos), 1 = parede/fora
    - comodos: letra -> conjunto de coordenadas
    - celula_para_comodo: célula -> letra do cômodo (ou None)
    - arestas_portas: pares de células adjacentes que cruzam de um cômodo a outro (portas)
    """
    linhas, colunas = 8, 8
    grade = [[1 for _ in range(colunas)] for _ in range(linhas)]  # tudo parede inicialmente

    comodos: Dict[str, Set[Coordenada]] = {
        "A": {(0,0), (0,1), (1,0), (1,1)},                    # 2x2
        "B": {(0,2), (1,2), (2,2)},                           # 3x1 (vertical)
        "C": {(0,3), (0,4), (1,3), (1,4)},                    # 2x2
        "D": {(3,0), (3,1), (3,2), (3,3)},                    # 1x4 (horizontal)
        "E": {(2,4), (3,4), (3,5), (4,5)},                    # formato L
        "F": {(4,1), (5,1)},                                  # 2x1 (vertical)
        "G": {(5,5), (5,6), (5,7)},                           # 1x3 (horizontal)
    }

    # Marca celulas de comodos como livres (0)
    for celulas in comodos.values():
        for (i, j) in celulas:
            grade[i][j] = 0

    # Mapeamento celula -> comodo
    celula_para_comodo: Dict[Coordenada, Optional[str]] = {}
    for nome, celulas in comodos.items():
        for c in celulas:
            celula_para_comodo[c] = nome
    for i in range(linhas):
        for j in range(colunas):
            if (i, j) not in celula_para_comodo:
                celula_para_comodo[(i, j)] = None

    # Portas: adjacencia 4-vizinhos entre celulas de comodos diferentes
    direcoes = [(-1,0),(1,0),(0,-1),(0,1)]
    arestas_portas: Set[frozenset] = set()
    for (i, j), r1 in celula_para_comodo.items():
        if r1 is None:
            continue
        for di, dj in direcoes:
            ni, nj = i+di, j+dj
            if 0 <= ni < linhas and 0 <= nj < colunas:
                r2 = celula_para_comodo[(ni, nj)]
                if r2 is not None and r2 != r1:
                    arestas_portas.add(frozenset({(i, j), (ni, nj)}))

    return grade, comodos, celula_para_comodo, arestas_portas

def ancora_comodo(comodos: Dict[str, Set[Coordenada]], c: str) -> Coordenada:
    """Escolhe uma celula ancora de um comodo (menor coordenada)."""
    return sorted(list(comodos[c]))[0]

# =========================
# Funcoes auxiliares de caminho e metricas
# =========================

def reconstruir_caminho(veio_de: Dict[Coordenada, Optional[Coordenada]], atual: Coordenada) -> List[Coordenada]:
    caminho: List[Coordenada] = []
    while atual is not None:
        caminho.append(atual)
        atual = veio_de[atual]
    return caminho[::-1]

def contar_cruzamentos_porta(caminho: List[Coordenada], celula_para_comodo: Dict[Coordenada, Optional[str]]) -> int:
    """Conta quantas vezes o caminho entra em um novo comodo (mudanca de comodo = 1 porta)."""
    if not caminho:
        return 0
    cruzamentos = 0
    ultimo_comodo: Optional[str] = celula_para_comodo.get(caminho[0])
    for c in caminho[1:]:
        r = celula_para_comodo.get(c)
        if r is not None and r != ultimo_comodo and ultimo_comodo is not None:
            cruzamentos += 1
        if r is not None:
            ultimo_comodo = r
    return cruzamentos

def resumir(nome: str, caminho: List[Coordenada],
            celula_para_comodo: Dict[Coordenada, Optional[str]], tempo_por_porta: float):
    if not caminho:
        print(f"{nome}: sem caminho.\n")
        return
    portas = contar_cruzamentos_porta(caminho, celula_para_comodo)
    tempo_total = portas * tempo_por_porta
    print(f"{nome}:")
    print(f"  - Tamanho do caminho (celulas): {len(caminho)}")
    print(f"  - Portas cruzadas: {portas}")
    print(f"  - Tempo total (s): {tempo_total:.2f}")
    print(f"  - Caminho: {caminho}\n")

# =========================
# Buscas no GRID (4-vizinhos) + instrumentacao
# =========================

def busca_gulosa(grade: List[List[int]], inicio: Coordenada, objetivo: Coordenada, *, detalhar: bool=False):
    """
    Busca Gulosa (Best-First) usando distancia de Manhattan. Se detalhar=True, imprime fronteira/visitados/grade.
    Retorna (caminho, metricas)
    """
    linhas, colunas = len(grade), len(grade[0])
    direcoes = [(-1,0), (1,0), (0,-1), (0,1)]

    fronteira: List[Tuple[int, Coordenada]] = [(distancia_manhattan(inicio, objetivo), inicio)]
    veio_de: Dict[Coordenada, Optional[Coordenada]] = {inicio: None}
    visitados: Set[Coordenada] = set()

    nos_expandidos = 0
    fronteira_tamanho_maximo = 1
    iteracoes = 0

    t0 = time.perf_counter()

    while fronteira:
        iteracoes += 1
        if detalhar:
            print(f"\n--- Iteracao {iteracoes} (Gulosa) ---")
            print("Fronteira (dist, pos):", [(dist, pos) for dist, pos in fronteira])
            print("Visitados:", sorted(list(visitados)))

        _, atual = heapq.heappop(fronteira)

        if atual == objetivo:
            t1 = time.perf_counter()
            caminho = reconstruir_caminho(veio_de, atual)
            metricas = {
                "algoritmo": "Busca Gulosa (Manhattan)",
                "encontrado": True,
                "tempo_segundos": t1 - t0,
                "nos_expandidos": nos_expandidos,
                "nos_visitados": len(visitados),
                "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
                "iteracoes": iteracoes,
                "tamanho_caminho": len(caminho)
            }
            return caminho, metricas

        if atual in visitados:
            continue
        visitados.add(atual)

        if detalhar:
            caminho_parcial = reconstruir_caminho(veio_de, atual)
            print("Grade (S=inicio, G=obj, #=obst, .=livre, C=atual, *=caminho):")
            imprimir_grade(grade, caminho_parcial, inicio, objetivo, atual)

        # expandir
        nos_expandidos += 1
        for dx, dy in direcoes:
            nx, ny = atual[0] + dx, atual[1] + dy
            if 0 <= nx < linhas and 0 <= ny < colunas and grade[nx][ny] == 0:
                prox = (nx, ny)
                if prox not in visitados:
                    heapq.heappush(fronteira, (distancia_manhattan(prox, objetivo), prox))
                    if prox not in veio_de:
                        veio_de[prox] = atual
        fronteira_tamanho_maximo = max(fronteira_tamanho_maximo, len(fronteira))

    t1 = time.perf_counter()
    metricas = {
        "algoritmo": "Busca Gulosa (Manhattan)",
        "encontrado": False,
        "tempo_segundos": t1 - t0,
        "nos_expandidos": nos_expandidos,
        "nos_visitados": len(visitados),
        "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
        "iteracoes": iteracoes,
        "tamanho_caminho": 0
    }
    return [], metricas

def busca_em_largura(grade: List[List[int]], inicio: Coordenada, objetivo: Coordenada):
    """Busca em Largura (otima em menor numero de passos). Retorna (caminho, metricas)."""
    linhas, colunas = len(grade), len(grade[0])
    direcoes = [(-1,0), (1,0), (0,-1), (0,1)]
    fila = deque([inicio])
    veio_de: Dict[Coordenada, Optional[Coordenada]] = {inicio: None}
    visitados: Set[Coordenada] = {inicio}

    nos_expandidos = 0
    fronteira_tamanho_maximo = 1
    iteracoes = 0
    t0 = time.perf_counter()

    while fila:
        iteracoes += 1
        u = fila.popleft()
        if u == objetivo:
            t1 = time.perf_counter()
            caminho = reconstruir_caminho(veio_de, u)
            metricas = {
                "algoritmo": "Busca em Largura (passos)",
                "encontrado": True,
                "tempo_segundos": t1 - t0,
                "nos_expandidos": nos_expandidos,
                "nos_visitados": len(visitados),
                "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
                "iteracoes": iteracoes,
                "tamanho_caminho": len(caminho)
            }
            return caminho, metricas
        # expandir
        nos_expandidos += 1
        for dx, dy in direcoes:
            nx, ny = u[0]+dx, u[1]+dy
            if 0 <= nx < linhas and 0 <= ny < colunas and grade[nx][ny] == 0:
                v = (nx, ny)
                if v not in visitados:
                    visitados.add(v)
                    veio_de[v] = u
                    fila.append(v)
        fronteira_tamanho_maximo = max(fronteira_tamanho_maximo, len(fila))

    t1 = time.perf_counter()
    metricas = {
        "algoritmo": "Busca em Largura (passos)",
        "encontrado": False,
        "tempo_segundos": t1 - t0,
        "nos_expandidos": nos_expandidos,
        "nos_visitados": len(visitados),
        "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
        "iteracoes": iteracoes,
        "tamanho_caminho": 0
    }
    return [], metricas

def busca_em_profundidade(grade: List[List[int]], inicio: Coordenada, objetivo: Coordenada):
    """Busca em Profundidade (nao garante otimo). Retorna (caminho, metricas)."""
    linhas, colunas = len(grade), len(grade[0])
    direcoes = [(-1,0), (1,0), (0,-1), (0,1)]
    pilha = [inicio]
    veio_de: Dict[Coordenada, Optional[Coordenada]] = {inicio: None}
    visitados: Set[Coordenada] = {inicio}

    nos_expandidos = 0
    fronteira_tamanho_maximo = 1
    iteracoes = 0
    t0 = time.perf_counter()

    while pilha:
        iteracoes += 1
        u = pilha.pop()
        if u == objetivo:
            t1 = time.perf_counter()
            caminho = reconstruir_caminho(veio_de, u)
            metricas = {
                "algoritmo": "Busca em Profundidade",
                "encontrado": True,
                "tempo_segundos": t1 - t0,
                "nos_expandidos": nos_expandidos,
                "nos_visitados": len(visitados),
                "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
                "iteracoes": iteracoes,
                "tamanho_caminho": len(caminho)
            }
            return caminho, metricas
        # expandir
        nos_expandidos += 1
        for dx, dy in direcoes:
            nx, ny = u[0]+dx, u[1]+dy
            if 0 <= nx < linhas and 0 <= ny < colunas and grade[nx][ny] == 0:
                v = (nx, ny)
                if v not in visitados:
                    visitados.add(v)
                    veio_de[v] = u
                    pilha.append(v)
        fronteira_tamanho_maximo = max(fronteira_tamanho_maximo, len(pilha))

    t1 = time.perf_counter()
    metricas = {
        "algoritmo": "Busca em Profundidade",
        "encontrado": False,
        "tempo_segundos": t1 - t0,
        "nos_expandidos": nos_expandidos,
        "nos_visitados": len(visitados),
        "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
        "iteracoes": iteracoes,
        "tamanho_caminho": 0
    }
    return [], metricas

# =========================
# A* (A estrela)
# =========================

def custo_transicao(u: Coordenada, v: Coordenada, celula_para_comodo: Dict[Coordenada, Optional[str]]) -> int:
    """
    Custo de transicao:
    - 0 se permanecer no mesmo comodo
    - 1 se cruzar de um comodo para outro (porta)
    """
    ru = celula_para_comodo.get(u)
    rv = celula_para_comodo.get(v)
    if ru is None or rv is None:
        return 10**6  # robustez
    return 0 if ru == rv else 1

def heuristica(a: Coordenada, b: Coordenada, celula_para_comodo: Dict[Coordenada, Optional[str]],
               modo: str = "manhattan") -> float:
    """
    Heuristica para A*:
    - 'manhattan'  -> distancia de Manhattan no grid (pode nao ser admissivel para custo por portas).
    - 'h1_comodo'  -> 0 se no mesmo comodo do objetivo, senao 1 (admissivel, porem fraca).
    - 'zero'       -> 0 (equivale a Dijkstra; sempre otimo, porem mais lento).
    """
    if modo == "manhattan":
        return float(distancia_manhattan(a, b))
    elif modo == "h1_comodo":
        return 0.0 if celula_para_comodo.get(a) == celula_para_comodo.get(b) else 1.0
    else:
        return 0.0

def busca_a_estrela(
    grade: List[List[int]],
    inicio: Coordenada,
    objetivo: Coordenada,
    celula_para_comodo: Dict[Coordenada, Optional[str]],
    modo_heuristica: str = "manhattan",
    detalhar: bool = False
):
    """A* com custo por porta (0 intra-comodo, 1 ao cruzar porta) e heuristica selecionavel.
       Retorna (caminho, metricas)."""
    linhas, colunas = len(grade), len(grade[0])
    direcoes = [(-1,0), (1,0), (0,-1), (0,1)]

    conjunto_aberto: List[Tuple[float, float, Coordenada]] = []
    custo_g: Dict[Coordenada, float] = {inicio: 0.0}
    f_inicio = heuristica(inicio, objetivo, celula_para_comodo, modo_heuristica)
    heapq.heappush(conjunto_aberto, (f_inicio, 0.0, inicio))
    veio_de: Dict[Coordenada, Optional[Coordenada]] = {inicio: None}
    conjunto_fechado: Set[Coordenada] = set()

    nos_expandidos = 0
    fronteira_tamanho_maximo = 1
    iteracoes = 0
    t0 = time.perf_counter()

    while conjunto_aberto:
        iteracoes += 1
        f, g, atual = heapq.heappop(conjunto_aberto)

        if detalhar:
            print(f"\n--- Iteracao {iteracoes} (A*) ---")
            print(f"Pop: atual={atual}, f={f:.3f}, g={g:.3f}")

        if atual == objetivo:
            t1 = time.perf_counter()
            caminho = reconstruir_caminho(veio_de, atual)
            metricas = {
                "algoritmo": f"A* ({modo_heuristica})",
                "encontrado": True,
                "tempo_segundos": t1 - t0,
                "nos_expandidos": nos_expandidos,
                "nos_visitados": len(conjunto_fechado),
                "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
                "iteracoes": iteracoes,
                "tamanho_caminho": len(caminho)
            }
            return caminho, metricas

        if atual in conjunto_fechado:
            continue
        conjunto_fechado.add(atual)

        # expandir
        nos_expandidos += 1
        for dx, dy in direcoes:
            nx, ny = atual[0] + dx, atual[1] + dy
            if not (0 <= nx < linhas and 0 <= ny < colunas):
                continue
            if grade[nx][ny] == 1:
                continue
            vizinho = (nx, ny)
            g_tentativo = custo_g[atual] + custo_transicao(atual, vizinho, celula_para_comodo)

            if vizinho not in custo_g or g_tentativo < custo_g[vizinho]:
                custo_g[vizinho] = g_tentativo
                veio_de[vizinho] = atual
                f_vizinho = g_tentativo + heuristica(vizinho, objetivo, celula_para_comodo, modo_heuristica)
                heapq.heappush(conjunto_aberto, (f_vizinho, g_tentativo, vizinho))
        fronteira_tamanho_maximo = max(fronteira_tamanho_maximo, len(conjunto_aberto))

    t1 = time.perf_counter()
    metricas = {
        "algoritmo": f"A* ({modo_heuristica})",
        "encontrado": False,
        "tempo_segundos": t1 - t0,
        "nos_expandidos": nos_expandidos,
        "nos_visitados": len(conjunto_fechado),
        "fronteira_tamanho_maximo": fronteira_tamanho_maximo,
        "iteracoes": iteracoes,
        "tamanho_caminho": 0
    }
    return [], metricas

# =========================
# Exportacao de metricas
# =========================

def exportar_metricas_csv(arquivo: str, linhas: List[Dict]):
    """Exporta metricas para CSV."""
    if not linhas:
        return
    colunas = [
        "algoritmo","encontrado","tempo_segundos","nos_expandidos","nos_visitados",
        "fronteira_tamanho_maximo","iteracoes","tamanho_caminho","portas_cruzadas","tempo_total"
    ]
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=colunas)
        escritor.writeheader()
        for r in linhas:
            escritor.writerow({c: r.get(c) for c in colunas})

# =========================
# Execucao
# =========================

def principal():
    # Constrói a planta
    grade, comodos, celula_para_comodo, arestas_portas = construir_grade_casa()

    # Escolha de origem/destino por comodo:
    comodo_origem = "A"
    comodo_destino = "G"
    inicio = ancora_comodo(comodos, comodo_origem)
    objetivo = ancora_comodo(comodos, comodo_destino)

    # Alternativamente, use coordenadas diretamente:
    # inicio = (0, 0)   # dentro de A
    # objetivo = (5, 7) # dentro de G

    tempo_por_porta = 5.0  # segundos por porta

    print("Grade inicial (S = inicio, G = objetivo, # = obstaculo, . = livre):")
    imprimir_grade(grade, [], inicio, objetivo)
    print("\nComodos e tamanhos:")
    for r in sorted(comodos.keys()):
        print(f"  {r}: {len(comodos[r])} celulas")
    print("Qtde. de portas (adjacencias entre comodos):", len(arestas_portas))
    print(f"\nOrigem (comodo): {comodo_origem} -> {inicio}")
    print(f"Destino (comodo): {comodo_destino} -> {objetivo}")
    print(f"Tempo por porta: {tempo_por_porta}s\n")

    # Executa buscas (coloque detalhar=True se quiser logs)
    caminho_gulosa, m_gulosa = busca_gulosa(grade, inicio, objetivo, detalhar=False)
    caminho_largura, m_largura = busca_em_largura(grade, inicio, objetivo)
    caminho_profundidade, m_profundidade = busca_em_profundidade(grade, inicio, objetivo)
    caminho_a_star, m_a_star = busca_a_estrela(grade, inicio, objetivo, celula_para_comodo,
                                               modo_heuristica="manhattan", detalhar=False)
    # (Opcional) A* com heuristica admissivel fraca:
    # caminho_a_star_h1, m_a_star_h1 = busca_a_estrela(grade, inicio, objetivo, celula_para_comodo,
    #                                                  modo_heuristica="h1_comodo", detalhar=False)

    # Resumo por algoritmo
    print("\n--- Resumo (caminhos e tempos) ---")
    for nome, caminho in [
        (m_gulosa["algoritmo"],         caminho_gulosa),
        (m_largura["algoritmo"],        caminho_largura),
        (m_profundidade["algoritmo"],   caminho_profundidade),
        (m_a_star["algoritmo"],         caminho_a_star),
        # (m_a_star_h1["algoritmo"],      caminho_a_star_h1),
    ]:
        resumir(nome, caminho, celula_para_comodo, tempo_por_porta)

    # Prepara metricas para exportacao
    linhas_metricas = []
    for m, caminho in [
        (m_gulosa,        caminho_gulosa),
        (m_largura,       caminho_largura),
        (m_profundidade,  caminho_profundidade),
        (m_a_star,        caminho_a_star),
        # (m_a_star_h1,     caminho_a_star_h1),
    ]:
        portas = contar_cruzamentos_porta(caminho, celula_para_comodo)
        linha = dict(m)
        linha["portas_cruzadas"] = portas
        linha["tempo_total"] = portas * tempo_por_porta
        linhas_metricas.append(linha)

    # Exporta para CSV
    # exportar_metricas_csv("metricas_saida.csv", linhas_metricas)
    # print("Metricas exportadas para: metricas_saida.csv")

if __name__ == "__main__":
    principal()
