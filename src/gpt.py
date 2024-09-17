import random
from typing import Tuple
import numpy as np
import pygame
import pymunk

# Inicializa o pygame e pymunk
pygame.init()

# Parâmetros da janela
width, height = 800, 600
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Criação do espaço de física do pymunk
space = pymunk.Space()
space.gravity = (0, -980)  # Gravidade padrão em pixels por segundo ao quadrado

# Definição da altura do fluido
fluid_height = height // 2  # Fluido ocupa metade da tela (ajuste conforme necessário)

class Ball():
    def __init__(self, radius: float, mass: float, position: Tuple[int, int], color=(255, 255, 255)):
        self.mass = mass
        self.volume = 4 / 3 * np.pi * radius**3
        self.color = color

        # Corpo físico e forma da bola
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.5

        self.body.angular_velocity = 0  # Zera a rotação
        self.body.moment = float("inf")  # Define o momento de inércia como infinito, impedindo rotação

        space.add(self.body, self.shape)

    def draw(self, screen: pygame.Surface):
        # Converte a posição pymunk para coordenadas pygame
        pos_x = int(self.body.position.x)
        pos_y = int(height - self.body.position.y)  # Inverte o eixo Y para o pygame
        pygame.draw.circle(screen, self.color, (pos_x, pos_y), int(self.shape.radius))

    def apply_buoyancy(self, fluid_height: int, fluid_density: float = 1.0, gravity: float = 9.8):
        # Calcula a profundidade submersa
        submersion_depth = max(0, fluid_height - self.body.position.y)
        if submersion_depth > 0:
            radius = self.shape.radius
            submersion_fraction = min(1, submersion_depth / (2 * radius))

            # Calcula o volume submerso
            submerged_volume = submersion_fraction * self.volume

            # Calcula a força de flutuação
            buoyancy_force = fluid_density * submerged_volume * gravity

            print(f"Buoyancy force: {buoyancy_force}")

            # Aplica a força de flutuação somente no eixo Y (positivo, para cima)
            self.body.apply_force_at_local_point((0, buoyancy_force))

    def apply_arrastro(self, fluid_height: int, drag_coefficient: float = 1.0):
        # Calcula a profundidade submersa
        submersion_depth = fluid_height - self.body.position.y

        if submersion_depth >= 0:  # A bola está acima da água
            # Calcula a força de arrasto somente para o eixo Y
            velocity_y = self.body.velocity.y
            drag_force_y = -drag_coefficient * velocity_y

            velocity_x = self.body.velocity.x
            drag_force_x = -drag_coefficient * velocity_x

            # Aplica a força de arrasto apenas no eixo Y (oposta ao movimento vertical)
            self.body.apply_force_at_local_point((drag_force_x * 20, drag_force_y * 100))

        else:
            # Se a bola estiver abaixo da linha da água, você pode aplicar arrasto
            # ou uma outra lógica específica para este caso
            pass

# Função para desenhar o nível do fluido
def draw_fluid_line(screen, fluid_height):
    pygame.draw.line(screen, (0, 0, 255), (0, height - fluid_height), (width, height - fluid_height), 2)

# Lista de bolas
balls = [Ball]

# Loop principal
running = True
while running:
    window.fill((0, 0, 0))

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Adiciona uma bola na posição do clique
            x, y = pygame.mouse.get_pos()
            offset_range = 2
            x_random = x + random.randint(-offset_range, offset_range)
            y_random = y + random.randint(-offset_range, offset_range)


            ball_radius = 10 # Raio aleatório entre 10 e 30
            ball_mass = 100  # Massa aleatória entre 1 e 10
            ball_color = (255, 255, 255)  # Cor branca
            new_ball = Ball(ball_radius, ball_mass, (x_random, height - y_random), ball_color)
            balls.append(new_ball)

    # Aplica a flutuação em cada bola e desenha as bolas
    for ball in balls:
        ball.apply_buoyancy(fluid_height)
        ball.apply_arrastro(fluid_height)
        ball.draw(window)

    # Desenha o nível do fluido
    draw_fluid_line(window, fluid_height)

    # Atualiza o espaço de física
    space.step(1 / 60.0)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
