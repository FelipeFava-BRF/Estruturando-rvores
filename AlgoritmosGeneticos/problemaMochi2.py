import random
import numpy as np

# Dados do problema
compartimentos = {
    'D': {'volume': 6800, 'peso': 10},
    'C': {'volume': 8700, 'peso': 16},
    'T': {'volume': 5300, 'peso': 8}
}

cargas = {
    'C1': {'volume_por_ton': 480, 'peso': 18, 'lucro': 310},
    'C2': {'volume_por_ton': 650, 'peso': 15, 'lucro': 380},
    'C3': {'volume_por_ton': 580, 'peso': 23, 'lucro': 350},
    'C4': {'volume_por_ton': 390, 'peso': 12, 'lucro': 285}
}

POP_SIZE = 100
NUM_GENERATIONS = 200
MUTATION_RATE = 0.1

def generate_individual():

    #retorna uma matriz 4x3 preenchida com zeros, 4 cargas x 3 compartimentos
    individual = np.zeros((4, 3))

    #cargas.values obtem todos os valores de carga
    for i, carga in enumerate(cargas.values()):
        remaining = carga['peso']
        for j in range(3):
            if j == 2:
                individual[i][j] = remaining
            else:
                part = round(random.uniform(0, remaining), 2)
                individual[i][j] = part
                remaining -= part
                
    return individual

def fitness(individual):
    lucro_total = 0
    volumes = [0, 0, 0]
    pesos = [0, 0, 0]

    for i, carga in enumerate(cargas.values()):
        for j in range(3):
            peso = individual[i][j]
            volume = peso * carga['volume_por_ton']
            lucro = peso * carga['lucro']
            volumes[j] += volume
            pesos[j] += peso
            lucro_total += lucro

    # Verifica restrições de volume e peso
    for j, comp in enumerate(compartimentos.values()):
        if volumes[j] > comp['volume'] or pesos[j] > comp['peso']:
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
    point = random.randint(1, 3)
    child = np.vstack((parent1[:point], parent2[point:]))
    return child

def mutate(individual):
    for i in range(4):
        if random.random() < MUTATION_RATE:
            j1, j2 = random.sample(range(3), 2)
            delta = round(random.uniform(-1, 1), 2)
            individual[i][j1] = max(0, individual[i][j1] + delta)
            individual[i][j2] = max(0, individual[i][j2] - delta)
    return individual

def genetic_algorithm():
    population = [generate_individual() for _ in range(POP_SIZE)]
    best_solution = None
    best_fitness = 0

    for generation in range(NUM_GENERATIONS):
        scored_population = [(ind, fitness(ind)) for ind in population]
        scored_population.sort(key=lambda x: x[1], reverse=True)

        if scored_population[0][1] > best_fitness:
            best_solution = scored_population[0][0]
            best_fitness = scored_population[0][1]

        selected = [ind for ind, score in scored_population[:POP_SIZE//2]]
        next_generation = []

        while len(next_generation) < POP_SIZE:
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_generation.append(child)

        population = next_generation

    return best_solution, best_fitness

solution, lucro = genetic_algorithm()

print("Distribuição ótima de cargas (em toneladas) por compartimento:")
for i, carga in enumerate(cargas.keys()):
    print(f"{carga}: D={solution[i][0]:.2f}, C={solution[i][1]:.2f}, T={solution[i][2]:.2f}")
print(f"Lucro total: R$ {lucro:.2f}")
