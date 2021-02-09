import random


def calculate_fitness(population, distance_matrix):
    fitness = []
    total_inverse_distances = []
    for i in population:
        d = 0
        for j in range(len(i)):
            d += distance_matrix[i[j]][i[(j + 1) % len(i)]]
        total_inverse_distances.append(1 / d)
    total_inverse_distance = sum(total_inverse_distances)
    for i in range(len(population)):
        fitness.append(total_inverse_distances[i] / total_inverse_distance)
    return fitness


def pick_one(population, fitness):
    x = random.random()
    s = 0
    for i in range(len(population)):
        s += fitness[i]
        if x < s:
            return population[i]
    return population[-1]


def crossover(parent_a, parent_b):
    a = random.randint(0, len(parent_a) - 1)
    b = random.randint(a, len(parent_a))
    if a == b:
        return parent_b[:]
    else:
        child = [-1] * len(parent_a)
        for i in range(a, b):
            child[i] = parent_a[i]
        i = 0
        for j in parent_b:
            if i == a:
                i = b
            if i >= len(parent_b):
                break
            if j not in child:
                child[i] = j
                i += 1
        return child


def mutate(child, mutate_rate=0.01):
    if random.random() < mutate_rate:
        a = random.randrange(len(child))
        b = random.randrange(len(child))
        child[a], child[b] = child[b], child[a]


def make_generation(population, fitness):
    new_population = []
    for i in range(len(population)):
        parent_a = pick_one(population, fitness)
        parent_b = pick_one(population, fitness)
        child = crossover(parent_a, parent_b)
        mutate(child)
        new_population.append(child)
    return new_population


best_ever = None
best_fitness = 0


def initialize_population(population_size, order_size):
    global best_ever
    global best_fitness
    best_ever = None
    best_fitness = 0
    population = []
    for i in range(population_size):
        v = list(range(order_size))
        random.shuffle(v)
        population.append(v)
    return population


def derive_population(population_size, order_size):
    global best_ever
    global best_fitness
    new_population = []
    size = population_size
    if best_ever:
        for i in range(order_size-1):
            new_order = best_ever[:i]+[order_size-1]+best_ever[i:]
            new_population.append(new_order)
            size -= 1

    best_ever = None
    best_fitness = 0

    for i in range(size):
        v = list(range(order_size))
        random.shuffle(v)
        new_population.append(v)
    return new_population


def run(population, distance_matrix):
    fitness = calculate_fitness(population, distance_matrix)
    if not fitness:
        return population
    x = max(fitness)
    global best_fitness
    global best_ever
    if best_fitness < x:
        best_fitness = x
        best_ever = population[fitness.index(x)]
    return make_generation(population, fitness)
