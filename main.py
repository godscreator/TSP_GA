import matplotlib
import pygame

import algorithm

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

fig1 = plt.figure(figsize=[3, 3])
ax1 = fig1.add_subplot(111)
canvas1 = agg.FigureCanvasAgg(fig1)
fig2 = plt.figure(figsize=[3, 3])
ax2 = fig2.add_subplot(111)
canvas2 = agg.FigureCanvasAgg(fig2)


def plot(x):
    ax2.clear()
    ax2.plot(list(range(1, len(x)+1)), x)
    canvas2.draw()
    renderer = canvas2.get_renderer()

    raw_data = renderer.tostring_rgb()
    size = canvas2.get_width_height()

    return pygame.image.fromstring(raw_data, size, "RGB")


def hist(y):
    ax1.clear()
    ax1.hist(y, bins=20)
    plt.gca().set(title="Fitness frequency", ylabel="Fitness")
    canvas1.draw()
    renderer = canvas1.get_renderer()

    raw_data = renderer.tostring_rgb()
    size = canvas1.get_width_height()

    return pygame.image.fromstring(raw_data, size, "RGB")


# initialize the pygame
pygame.init()

# create the screen
screenX = 790
screenY = 790
screen = pygame.display.set_mode((screenX, screenY))

# Title and Icon
pygame.display.set_caption("Travelling Salesman")

# cities
cities = []


def draw_cities(cities, offset=(0, 0)):
    for city in cities:
        pygame.draw.circle(screen, (255, 0, 0), (city.x + offset[0], city.y + offset[1]), 4)
        pygame.draw.circle(screen, (255, 0, 0), (city.x + offset[0], city.y + offset[1]), 10, width=1)


# roads
population = []


def draw_roads(order, offset=(0, 0), color=(255, 255, 255)):
    if order and len(order) >= 2:
        for i in range(len(order)):
            a = cities[order[i]]
            b = cities[order[(i + 1) % len(order)]]
            pygame.draw.line(screen, color, (a.x + offset[0], a.y + offset[1]), (b.x + offset[0], b.y + offset[1]))


clock = pygame.time.Clock()
tsp = algorithm.TSP(population_size=100)
count = 0
best_road = None

rect1 = pygame.Rect(10, 10, 380, 380)
best_panel = (10, 10, 380, 380)
rect2 = pygame.Rect(10, 400, 380, 380)
population_panel = (10, 400, 380, 380)
rect3 = pygame.Rect(400, 10, 380, 380)
update_panel = (400, 10, 380, 380)
rect4 = pygame.Rect(400, 400, 380, 380)
generation_panel = (400, 400, 380, 380)

# text
font = pygame.font.Font('freesansbold.ttf', 16)


def draw_text(s, pos):
    text = font.render(s, True, (127, 0, 0))
    screen.blit(text, pos)


generation_number = 0
generation_distance = []
best_fitness = None
best_distance_all = None
# Game Loop
running = True
while running:
    # background
    screen.fill((127, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), rect1)
    pygame.draw.rect(screen, (255, 255, 255), rect2)
    pygame.draw.rect(screen, (255, 255, 255), rect3)
    pygame.draw.rect(screen, (255, 255, 255), rect4)
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if best_panel[0] < x < best_panel[0] + best_panel[2] and best_panel[1] < y < best_panel[1] + best_panel[3]:
                # add a new city
                new_city = algorithm.City(x, y)
                tsp.add_city(new_city)
                cities = tsp.cities
                tsp.derive_population()
                population = tsp.population
                generation_number = 0
                generation_distance.clear()
    if len(tsp.cities) >= 2 and count == len(population) - 1:
        tsp.calculate_fitness()
        tsp.make_generation()
        tsp.calculate_fitness()
        population = tsp.population
        generation_number += 1
        road = tsp.get_best_gene()
        best_fitness = tsp.get_best_fitness()
        if road:
            best_road = road
            best_distance = tsp.calculate_distance(tsp.get_best_gene())
            generation_distance.append(best_distance)
            best_distance_all = min(generation_distance)

    # display Best
    draw_cities(cities)
    draw_roads(best_road, color=(0, 255, 0))
    draw_text("Previous best", (best_panel[0], best_panel[1]))

    # display all population
    draw_cities(cities, offset=(update_panel[0], update_panel[1]))
    if population:
        road = population[count]
        count = (count + 1) % len(population)
        draw_roads(road, color=(0, 0, 255), offset=(update_panel[0], update_panel[1]))
        draw_text("Generation:" + str(generation_number), (update_panel[0], update_panel[1]))

    # display graph
    draw_text(" Frequency distribution  of parent fitness", (population_panel[0], population_panel[1]))
    if len(cities) >= 2 and tsp.parent_fitness:
        graph1 = hist(tsp.parent_fitness)
        screen.blit(graph1, (population_panel[0] + 40, population_panel[1] + 40))

    # display graph
    draw_text("best distance (y) vs generation(x)", (generation_panel[0], generation_panel[1]))
    if best_distance_all:
        draw_text(" best Distance = " + str(best_distance_all), (generation_panel[0], generation_panel[1] + 18))
    if len(cities) >= 2 and tsp.fitness:
        graph2 = plot(generation_distance)
        screen.blit(graph2, (generation_panel[0] + 40, generation_panel[1] + 40))
    pygame.display.update()
