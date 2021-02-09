import pygame
import algorithm

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
font = pygame.font.Font('freesansbold.ttf', 32)


def draw_text(s, pos):
    text = font.render(s, True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = pos
    screen.blit(text, textRect)


# draw graph
def draw_graph(range_x, range_y, f, panel, div_x, div_y, scale_x, scale_y):
    screen_origin = (panel[0] + 20, panel[1] + panel[3] - 20)
    y_origin = screen_origin[1]
    y_max = screen_origin[1] - panel[3] + 30
    x_origin = screen_origin[0]
    x_max = screen_origin[0] + panel[1] - 50
    screen_scale_x = (x_max - x_origin) / (range_x[1] - range_x[0])
    screen_scale_y = (y_max - y_origin) / (range_y[1] - range_y[0])
    # y axis
    pygame.draw.line(screen, (0, 0, 0), screen_origin, (x_origin, y_max))
    # x axis
    pygame.draw.line(screen, (0, 0, 0), screen_origin, (x_max, y_origin))
    # label x axis
    for i in range()


# Game Loop
running = True
while running:
    # background
    screen.fill((255, 0, 0))
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
                tsp.derive_population()
                cities = tsp.cities
                population = tsp.population
    if len(tsp.cities) >= 2 and count == len(population) - 1:
        tsp.calculate_fitness()
        tsp.make_generation()
        tsp.calculate_fitness()
        population = tsp.population

    # display Best
    draw_cities(cities)
    road = tsp.get_best_gene()
    fitness = tsp.get_best_fitness()
    if road:
        best_road = road
    draw_roads(best_road, color=(0, 255, 0))

    # display all population
    draw_cities(cities, offset=(update_panel[0], update_panel[1]))
    if population:
        road = population[count]
        count = (count + 1) % len(population)
        draw_roads(road, color=(0, 0, 255), offset=(update_panel[0], update_panel[1]))

    # display population graph
    draw_graph(None,None,None,population_panel)
    pygame.display.update()
    clock.tick(40)
