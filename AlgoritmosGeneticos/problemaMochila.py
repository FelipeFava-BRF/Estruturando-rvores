# tentar implementar resolução por força bruta e backtracking

import random
import numpy as np

# Dados do problema
compartimentos = {
    'D': {'volume': 6800, 'peso': 10},
    'C': {'volume': 8700, 'peso': 16},
    'T': {'volume': 5300, 'peso': 8}
}

# o volume dos compartimentos é o volume total suportado, não o volume por tonelada.

# talvez usar 18000Kg ao invés de 18T para representar o tamanho do número
cargas = {
    'C1': {'volume_por_ton': 480, 'peso': 18, 'lucro': 310},
    'C2': {'volume_por_ton': 650, 'peso': 15, 'lucro': 380},
    'C3': {'volume_por_ton': 580, 'peso': 23, 'lucro': 350},
    'C4': {'volume_por_ton': 390, 'peso': 12, 'lucro': 285}
}

# Nota
# usar o cálculo lucro = volume_por_ton x peso parece estranho. Pois não temos a informações de quanto tirar do peso para se obter tal volume e lucro
# pegando C3 de exemplo, só sabemos que com o volume por tonelada igual a 580, temos o peso total de 23 e o lucro de 350.
# Do C3, o volume total considerando todas as toneladas (peso) é volume total = volume por tonelada x peso -> volume total = 580 x 23 -> volume total = 13.340

TAM_POPULACAO = 100
NUM_GERACOES = 200
TAXA_MUTACAO = 0.1

def gerar_individuo():

    #retorna uma matriz 4x3 preenchida com zeros, 4 cargas x 3 compartimentos
    individual = np.zeros((4, 3))

    #cargas.values obtem todos os valores de carga
    for i, carga in enumerate(cargas.values()):
        restante = carga['peso']

        for j in range(3):
            if j == 2:
                individual[i][j] = restante
            else:
                # random.uniform gera um valor float aleatório entre 0 e o peso da carga
                # round arredonda o valor float para até 3 casas decimais (conversão Ton para Kg)
                part = round(random.uniform(0, restante), 3)
                individual[i][j] = part
                restante -= part

    return individual

def fitness(individual):
    lucro_total = 0
    volumes = [0, 0, 0] # volume usado em cada compartimento (D, C, T)
    pesos = [0, 0, 0] # peso usado em cada compartimento (D, C, T)

    for i, carga in enumerate(cargas.values()): 
        for j in range(3):
            peso = individual[i][j]                                     # toneladas da carga i no compartimento j
            volume = peso * carga['volume_por_ton']                     # volume consumido
            lucro = peso * carga['lucro']                               # lucro gerado
            volumes[j] += volume
            pesos[j] += peso
            lucro_total += lucro

    # Verifica restrições de volume e peso
    for j, comp in enumerate(compartimentos.values()):
        if volumes[j] > comp['volume'] or pesos[j] > comp['peso']:
            # se o volume ou o peso calculado for maior do que o suportado pelo avião atribui 0 de fitness, pois não é uma solução boa
            # talvez esse retorno não esteja certo, pois não possibilita recalcular o fitness e atribuir penalização
            return 0

    # Penalização por desequilíbrio
    total_volume = sum([comp['volume'] for comp in compartimentos.values()])
    total_peso = sum(pesos)
    excesso_total = 0
    for j, comp in enumerate(compartimentos.values()):
        proporcao_volume = comp['volume'] / total_volume
        proporcao_peso = pesos[j] / total_peso if total_peso > 0 else 0
        excesso = abs(proporcao_volume - proporcao_peso)
        if excesso > 0.05:
            excesso_total += excesso

    if excesso_total > 0:
        lucro_total *= (1 - excesso_total)

    return lucro_total

def crossover(parent1, parent2):
    point = random.randint(1, 3) # gera número aleatório entre 1, 2 e 3, nesse caso, o point está sendo usado para fazer um corte nas linhas (vetores)
    # np.stack empilha vetores de cima para baixo, parecendo uma matriz, nesse caso formando o filho com algumas linhas do pai1 e o restante do pai2.
    child = np.vstack((parent1[:point],  # linhas [0 .. point -1] primeiras point linhas do pai1
                       parent2[point:])) # linhas [point .. fim] da linha point até o fim do pai2
    
    # Ex.: se point = 2, o filho terá:
    # Linhas 0 e 1 do pai1
    # Linhas 2 e 3 do pai2

    return child

def mutate(individual):
    for i in range(4):
        if random.random() < TAXA_MUTACAO:
            j1, j2 = random.sample(range(3), 2)
            
            # delta é uma pequena variação aleatória (entre -1 e 1 toneladas) aplicada a uma linha (uma carga específica), arredondado para 2 casas decimais
            delta = round(random.uniform(-1, 1), 2)
            # para explorar novos vizinhos
            # Aumenta j1 e diminui j2 (para tentar manter a soma da linha parecida)
            individual[i][j1] = max(0, individual[i][j1] + delta) # max impede que os números sejam negativos, max = maior valor entre 0 e o calculado com delta
            individual[i][j2] = max(0, individual[i][j2] - delta)

    return individual

def algoritmo_genetico():
    # cria população inicial com indivíduos aleatórios
    populacao = [gerar_individuo() for _ in range(TAM_POPULACAO)]
    
    # para elitismo - verificar
    melhor_solucao = None
    melhor_fitness = 0

    for geracao in range(NUM_GERACOES):
        scored_populacao = [(ind, fitness(ind)) for ind in populacao]
        scored_populacao.sort(key=lambda x: x[1], reverse=True)

        if scored_populacao[0][1] > melhor_fitness:
            melhor_solucao = scored_populacao[0][0]
            melhor_fitness = scored_populacao[0][1]

        selecionados = [ind for ind, score in scored_populacao[:TAM_POPULACAO//2]] # divisão inteira da população pela metade
        prox_geracao = []

        while len(prox_geracao) < TAM_POPULACAO:
            p1, p2 = random.sample(selecionados, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            prox_geracao.append(child)

        populacao = prox_geracao

    return melhor_solucao, melhor_fitness

solution, lucro = algoritmo_genetico()

print("Distribuição ótima de cargas (em toneladas) por compartimento:")
for i, carga in enumerate(cargas.keys()):
    print(f"{carga}: D={solution[i][0]:.2f}, C={solution[i][1]:.2f}, T={solution[i][2]:.2f}")
print(f"Lucro total: R$ {lucro:.2f}")
