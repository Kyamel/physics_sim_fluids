import pygame
import pymunk
import pymunk.pygame_util
import random

# Função para converter coordenadas pymunk -> pygame


def pymunk_to_pygame(p):
    return int(p.x), int(HEIGHT - p.y)


# Configurações da tela
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PARTICLE_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)
LINE_COLOR = (255, 0, 0)

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Fluidos 2D com pymunk")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)  # Fonte para exibir o FPS

# Inicialização do espaço físico com Chipmunk
space = pymunk.Space()
space.gravity = (0, -1000)  # Gravidade negativa para baixo

# Adicionar o "chão" como uma linha estática
# Linha na parte inferior da tela
ground = pymunk.Segment(space.static_body, (0, 10), (WIDTH, 10), 5)
ground.elasticity = 0.5
ground.friction = 0.5
space.add(ground)

# Adicionar paredes laterais como linhas estáticas
left_wall = pymunk.Segment(space.static_body, (10, 0), (10, HEIGHT), 5)
right_wall = pymunk.Segment(
    space.static_body, (WIDTH - 10, 0), (WIDTH - 10, HEIGHT), 5)
left_wall.elasticity = 0.5
right_wall.elasticity = 0.5
left_wall.friction = 0.5
right_wall.friction = 0.5
space.add(left_wall, right_wall)

# Cria uma rampa estática (segmento inclinado)
ramp_start = (50, 100)
ramp_end = (300, 200)
ramp = pymunk.Segment(space.static_body, ramp_start, ramp_end, 5)
ramp.friction = 1.0
space.add(ramp)

# Criando uma superficie quadrada
square_body = pymunk.Body(body_type=pymunk.Body.STATIC)
square_shape1 = pymunk.Segment(square_body, (30, 100), (30, 200), 5)


# Função para adicionar partículas
def add_particle(x, y):
    x = random.uniform(x-0.1, x+0.1)
    y = random.uniform(y-0.1, y+0.1)
    mass = 1
    inertia = pymunk.moment_for_circle(
        mass, 0, 5)  # Momento de inércia, raio 5
    body = pymunk.Body(mass, inertia)
    body.position = x, HEIGHT - y  # Ajusta para posição invertida do Pygame
    shape = pymunk.Circle(body, 5)  # Raio 5 para a partícula
    shape.elasticity = 0.5
    shape.friction = 0.5
    space.add(body, shape)
    return shape


# Lista de partículas
particles = []

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            particle_shape = add_particle(x, y)
            particles.append(particle_shape)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x, y = pygame.mouse.get_pos()
        particle_shape = add_particle(x, y)
        particles.append(particle_shape)

    screen.fill(BACKGROUND_COLOR)

    # Simulação física
    space.step(1 / 60.0)

    # Desenhar partículas
    for particle in particles:
        pos_x = int(particle.body.position.x)
        # Inverte a posição para o Pygame
        pos_y = int(HEIGHT - particle.body.position.y)
        pygame.draw.circle(screen, PARTICLE_COLOR, (pos_x, pos_y), 10)

    # Desenhar o "chão"
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - 10),
                     (WIDTH, HEIGHT - 10), 5)
    # Desenhar paredes (linhas estáticas)
    pygame.draw.line(screen, LINE_COLOR, (10, 0), (10, HEIGHT), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - 10, 0),
                     (WIDTH - 10, HEIGHT), 5)
    # Desenhar a rampa
    pygame.draw.line(screen, LINE_COLOR, pymunk_to_pygame(
        ramp.a), pymunk_to_pygame(ramp.b), 5)

    # Desenhando a superfície quadrada
    pygame.draw.line(screen, LINE_COLOR, (30, 100), (30, 200), 5)

    # Calcular e exibir o FPS
    fps = clock.get_fps()
    fps_text = font.render(f" FPS: {int(fps)}", True, TEXT_COLOR)
    particle_count = font.render(
        f" Particle Count: {len(particles)}", True, TEXT_COLOR)
    screen.blit(particle_count, (10, 30))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
