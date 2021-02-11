import random
import math


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance(A, B):
        return math.sqrt(math.pow(A.x - B.x, 2) + math.pow(A.y - B.y, 2))


class Path:
    # class properties
    cities = []
    distance_matrix = []

    @classmethod
    def add_city(cls, new_city):
        # adding new city to cities
        cls.cities.append(new_city)
        # adding new city column
        for i in range(len(cls.cities) - 1):
            cls.distance_matrix[i].append(City.get_distance(cls.cities[i], new_city))
        # adding new city row
        cls.distance_matrix.append([])
        for i in range(len(cls.cities) - 1):
            cls.distance_matrix[-1].append(cls.distance_matrix[i][-1])
        cls.distance_matrix[-1].append(0)

    @classmethod
    def calculate_distances(cls):
        if len(cls.cities) > 0:
            cls.distance_matrix = [[-1] * len(cls.cities) for i in range(len(cls.cities))]
            # calculate distance matrix
            for i in range(len(cls.cities)):
                for j in range(len(cls.cities)):
                    if cls.distance_matrix[j][i] == -1:
                        d = City.get_distance(cls.cities[i], cls.cities[j])
                        cls.distance_matrix[i][j] = d
                    else:
                        cls.distance_matrix[i][j] = cls.distance_matrix[j][i]

    # instance properties
    def __init__(self, order=[], randomized=False):
        self.order = order
        if randomized:
            v = list(range(len(Path.cities)))
            random.shuffle(v)
            self.order = v
        self.distance = self.calculate_distance()

    def calculate_distance(self):
        d = 0
        for j in range(len(self.order)):
            d += Path.distance_matrix[self.order[j]][self.order[(j + 1) % len(self.order)]]
        return d

    def mutate(self, mutate_rate):
        if random.random() < mutate_rate:
            a = random.randrange(len(self.order))
            b = random.randrange(len(self.order))
            self.order[a], self.order[b] = self.order[b], self.order[a]

    @staticmethod
    def crossover(parent_a, parent_b):
        a = random.randint(0, len(parent_a.order) - 1)
        b = random.randint(a, len(parent_a.order))
        if a == b:
            return Path(parent_b.order[:])
        else:
            child = [-1] * len(parent_a.order)
            for i in range(a, b):
                child[i] = parent_a.order[i]
            i = 0
            for j in parent_b.order:
                if i == a:
                    i = b
                if i >= len(parent_b.order):
                    break
                if j not in child:
                    child[i] = j
                    i += 1
            return Path(child)


class TSP:
    def __init__(self, population_size=10):
        self.population_size = population_size
        self.population = []
        self.fitness = []
        self.current_distances = []
        self.parent_fitness = []
        self.initialize_population()

    def initialize_population(self):
        self.population = []
        for i in range(self.population_size):
            v = Path(randomized=True)
            self.population.append(v)

    def calculate_fitness(self):
        fitness = []
        total_inverse_distances = []
        self.current_distances = []
        for i in self.population:
            d = i.distance
            self.current_distances.append(d)
            total_inverse_distances.append(1 / (d * d))
        total_inverse_distance = sum(total_inverse_distances)
        for i in range(len(self.population)):
            x = total_inverse_distances[i] / total_inverse_distance
            fitness.append(x)
        self.fitness = fitness

    def pick_one(self):
        x = random.random()
        s = 0
        for i in range(len(self.population)):
            s += self.fitness[i]
            if x < s:
                return self.population[i]
        return self.population[-1]

    def make_generation(self):
        new_population = []
        self.parent_fitness = []
        for i in range(len(self.population)):
            parent_a = self.pick_one()
            parent_b = self.pick_one()
            self.parent_fitness.append(parent_a.distance)
            self.parent_fitness.append(parent_b.distance)
            child = Path.crossover(parent_a, parent_b)
            child.mutate(mutate_rate=0.01)
            new_population.append(child)
        self.population = new_population

    def derive_population(self, size=None):
        best_ever = self.get_best_gene()
        new_population = []
        if size:
            self.population_size = size
        else:
            size = self.population_size
        order_size = len(Path.cities)
        if best_ever:
            for i in range(order_size - 1):
                new_order = best_ever.order[:i] + [order_size - 1] + best_ever.order[i:]
                new_population.append(Path(new_order))
                size -= 1
        for i in range(size):
            v = Path(randomized=True)
            new_population.append(v)
        self.population = new_population

    def get_best_index(self):
        if self.fitness:
            return self.fitness.index(max(self.fitness))
        else:
            return None

    def get_best_gene(self):
        ind = self.get_best_index()
        if ind is not None:
            return self.population[ind]
        else:
            return None

    def get_best_fitness(self):
        ind = self.get_best_index()
        if ind is not None:
            return self.fitness[ind]
        else:
            return None
