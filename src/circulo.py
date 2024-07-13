import pymunk
import pygame
import math

def create_semicircle(body, radius, segments):
    points = []
    for i in range(segments + 1):
        angle = math.pi * i / segments  # Angulo varia de 0 a pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
    points.append((0, 0))  # Adiciona o centro para completar o semicírculo
    
    shape = pymunk.Poly(body, points)
    return shape

# Inicializa o Pygame e pymunk
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -900)

# Cria o corpo e o semicírculo
mass = 1
radius = 50
segments = 20  # Número de segmentos para aproximar o semicírculo
inertia = pymunk.moment_for_circle(mass, 0, radius)
body = pymunk.Body(mass, inertia)
body.position = (300, 300)
semicircle_shape = create_semicircle(body, radius, segments)
semicircle_shape.friction = 0.5
semicircle_shape.elasticity = 0.5
space.add(body, semicircle_shape)

# Loop principal do Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    space.step(1/50.0)
    screen.fill((255, 255, 255))
    
    # Desenha o semicírculo
    vertices = semicircle_shape.get_vertices()
    points = [(v.rotated(body.angle) + body.position) for v in vertices]
    points = [(p.x, 600 - p.y) for p in points]  # Ajusta a posição y para a coordenada do Pygame
    pygame.draw.polygon(screen, (255, 0, 0), points)
    
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
