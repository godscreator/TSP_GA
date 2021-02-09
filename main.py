import pygame
import math
import algorithm

# initialize the pygame
pygame.init()

# create the screen
screenX = 600
screenY = 800
screen = pygame.display.set_mode((screenX, screenY))

# Title and Icon
pygame.display.set_caption("Travelling Salesman")


# cities
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self, offset=(0, 0)):
        pygame.draw.circle(screen, (255, 0, 0), (self.x+offset[0], self.y+offset[1]), 4)
        pygame.draw.circle(screen, (255, 0, 0), (self.x+offset[0], self.y+offset[1]), 10, width=1)


# roads
def make_road(x1, y1, x2, y2):
    pygame.draw.line(screen, (0, 255, 0), (x1, y1), (x2, y2))


def make_bad_road(x1, y1, x2, y2):
    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))


# distance matrix
distance_matrix = []


def get_distance(city_A, city_B):
    return math.sqrt(math.pow(city_A.x - city_B.x, 2) + math.pow(city_A.y - city_B.y, 2))


def update_distance_matrix(cities, new_city):
    distance_matrix.append([])
    for i in range(len(cities) - 1):
        distance_matrix[i].append(get_distance(cities[i], new_city))
    for i in range(len(cities) - 1):
        distance_matrix[-1].append(distance_matrix[i][-1])
    distance_matrix[-1].append(0)


cities = []
population = []
count = 0
x = True
# Game Loop
running = True
while running:
    # background
    screen.fill((0, 0, 0))
    if x:
        pygame.draw.circle(screen, (255, 255, 255), (0, 0), 20)
    x = not x
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            new_city = City(x, y)
            cities.append(new_city)
            update_distance_matrix(cities, new_city)
            if len(cities) >= 2:
                population = algorithm.derive_population(1000, len(cities))
    if len(cities) >= 2 and count == len(population)-1:
        population = algorithm.run(population, distance_matrix)
    # all cities
    for i in cities:
        i.show()
    # roads
    road = algorithm.best_ever
    if road and len(road) >= 2:
        for i in range(len(road)):
            a = road[i]
            b = road[(i + 1) % len(road)]
            make_road(cities[a].x, cities[a].y, cities[b].x, cities[b].y)

    # all cities
    for i in cities:
        i.show(offset=(0, 300))
    if population:
        road = population[count]
        count = (count + 1) % len(population)
    if road and len(road) >= 2:
        for i in range(len(road)):
            a = road[i]
            b = road[(i + 1) % len(road)]
            make_bad_road(cities[a].x, cities[a].y+300, cities[b].x, cities[b].y+300)
    # # all roads
    # for i in cities:
    #     for j in cities:
    #         if i!=j:
    #             make_road(i.x, i.y, j.x, j.y)

    pygame.display.update()
