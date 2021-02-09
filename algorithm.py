import random
import math


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance(A, B):
        return math.sqrt(math.pow(A.x - B.x, 2) + math.pow(A.y - B.y, 2))


class TSP:
    def __init__(self, population_size=10, cities=[]):
        self.cities = cities
        self.distance_matrix = []
        self.calculate_distances()

        self.population_size = population_size
        self.population = []
        self.fitness = []
        self.initialize_population()

    def calculate_distances(self):
        if len(self.cities) > 0:
            self.distance_matrix = [[-1] * len(self.cities) for i in range(len(self.cities))]
            # calculate distance matrix
            for i in range(len(self.cities)):
                for j in range(len(self.cities)):
                    if self.distance_matrix[j][i] == -1:
                        d = City.get_distance(self.cities[i], self.cities[j])
                        self.distance_matrix[i][j] = d
                    else:
                        self.distance_matrix[i][j] = self.distance_matrix[j][i]

    def initialize_population(self):
        order_size = len(self.cities)
        population_size = self.population_size
        self.population = []
        for i in range(population_size):
            v = list(range(order_size))
            random.shuffle(v)
            self.population.append(v)

    def calculate_fitness(self):
        fitness = []
        total_inverse_distances = []
        for i in self.population:
            d = 0
            for j in range(len(i)):
                d += self.distance_matrix[i[j]][i[(j + 1) % len(i)]]
            total_inverse_distances.append(1 / d)
        total_inverse_distance = sum(total_inverse_distances)
        for i in range(len(self.population)):
            fitness.append(total_inverse_distances[i] / total_inverse_distance)
        self.fitness = fitness

    def add_city(self, new_city):
        self.cities.append(new_city)
        self.distance_matrix.append([])
        for i in range(len(self.cities) - 1):
            self.distance_matrix[i].append(City.get_distance(self.cities[i], new_city))
        for i in range(len(self.cities) - 1):
            self.distance_matrix[-1].append(self.distance_matrix[i][-1])
        self.distance_matrix[-1].append(0)

    def pick_one(self):
        x = random.random()
        s = 0
        for i in range(len(self.population)):
            s += self.fitness[i]
            if x < s:
                return self.population[i]
        return self.population[-1]

    @staticmethod
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

    @staticmethod
    def mutate(child, mutate_rate=0.01):
        if random.random() < mutate_rate:
            a = random.randrange(len(child))
            b = random.randrange(len(child))
            child[a], child[b] = child[b], child[a]

    def make_generation(self):
        new_population = []
        for i in range(len(self.population)):
            parent_a = self.pick_one()
            parent_b = self.pick_one()
            child = TSP.crossover(parent_a, parent_b)
            TSP.mutate(child)
            new_population.append(child)
        self.population = new_population

    def derive_population(self):
        best_ever = self.get_best_gene()
        new_population = []
        size = self.population_size
        order_size = len(self.cities)
        if best_ever:
            for i in range(order_size - 1):
                new_order = best_ever[:i] + [order_size - 1] + best_ever[i:]
                new_population.append(new_order)
                size -= 1
        for i in range(size):
            v = list(range(order_size))
            random.shuffle(v)
            new_population.append(v)
        self.population = new_population

    def get_best_index(self):
        if self.fitness:
            return self.fitness.index(max(self.fitness))
        else:
            return None

    def get_best_gene(self):
        ind = self.get_best_index()
        if ind:
            return self.population[ind]
        else:
            return None

    def get_best_fitness(self):
        ind = self.get_best_index()
        if ind:
            return self.fitness[ind]
        else:
            return None
