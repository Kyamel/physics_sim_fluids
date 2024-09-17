import random
import time
from typing import List, Tuple
import pygame
import pymunk
import pygame_gui

# Inicializa o pygame e pymunk
pygame.init()

# Parâmetros da janela
width, height = 800, 600
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Criação do espaço de física do pymunk
space = pymunk.Space()
space.gravity = (0, -980)  # Gravidade padrão em pixels por segundo ao quadrado

# Inicializa o pygame_gui
manager = pygame_gui.UIManager((width, height))

# Definição da altura do fluido
fluid_height = height // 2  # Fluido ocupa metade da tela (ajuste conforme necessário)
fluid_density = 1.0

# GUI: Criar sliders para modificar propriedades do fluido e da bola
fluid_height_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 50), (200, 25)),
    start_value=fluid_height,
    value_range=(0, height),
    manager=manager
)

fluid_density_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 100), (200, 25)), 
    start_value=fluid_density,
    value_range=(0.0, 10.0),
    manager=manager
)

ball_density_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 150), (200, 25)),
    start_value=5.0,  # Valor inicial
    value_range=(0.0, 10.0),  # Ajuste o intervalo conforme necessário
    manager=manager
)

class Ball():
    def __init__(self, radius: float, density: float, position: Tuple[int, int], color=(255, 255, 255)):
        self.volume = 1  # volume constante para que a massa seja = densidade
        self.mass = density
        self.color = color
        self.radius = 10

        # Corpo físico e forma da bola
        self.body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, radius))
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

    def apply_buoyancy(self, fluid_height: int, fluid_density: float = 1.0, gravity: float = -980):
        # Calcula a profundidade submersa
        submersion_depth = max(0, fluid_height - self.body.position.y)
        if submersion_depth > 0:
            radius = self.shape.radius
            submersion_fraction = min(1, submersion_depth / (2 * radius))

            # Calcula o volume submerso
            submerged_volume = submersion_fraction * self.volume

            # Calcula a força de flutuação
            buoyancy_force = fluid_density * 1 * gravity

            # Aplica a força de flutuação somente no eixo Y (positivo, para cima) ao contrário da gravidade
            self.body.apply_force_at_local_point((0, -buoyancy_force))

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

    def is_mouse_over(self, mouse_pos: Tuple[int, int]) -> bool:
        ball_pos = (int(self.body.position.x), int(height - self.body.position.y))
        distance = ((mouse_pos[0] - ball_pos[0]) ** 2 + (mouse_pos[1] - ball_pos[1]) ** 2) ** 0.5
        return distance <= self.radius

# Função para desenhar o nível do fluido
def draw_fluid_line(screen, fluid_height):
    pygame.draw.line(screen, (0, 0, 255), (0, height - fluid_height), (width, height - fluid_height), 2)

# Função para criar as paredes ao redor da tela
def create_walls():
    wall_thickness = 10  # Espessura das paredes

    walls = [
        # Parede superior
        pymunk.Segment(space.static_body, (0, height - wall_thickness), (width, height - wall_thickness), wall_thickness),
        # Parede inferior
        pymunk.Segment(space.static_body, (0, wall_thickness), (width, wall_thickness), wall_thickness),
        # Parede esquerda
        pymunk.Segment(space.static_body, (wall_thickness, 0), (wall_thickness, height), wall_thickness),
        # Parede direita
        pymunk.Segment(space.static_body, (width - wall_thickness, 0), (width - wall_thickness, height), wall_thickness)
    ]

    for wall in walls:
        wall.friction = 1.0
        wall.elasticity = 0.8
        space.add(wall)

create_walls()

# Lista de bolas
balls: List[Ball] = []

# Variável para armazenar a densidade da bola atual
current_ball_density = 5.0

tooltip = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 0), (100, 30)),
        text='',
        manager=manager
    )

# Loop principal
running = True
while running:
    time_delta = clock.tick(100) / 1000.0
    window.fill((0, 0, 0))

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Adiciona uma bola na posição do clique
            x, y = pygame.mouse.get_pos()
            offset_range = 2
            x_random = x + random.randint(-offset_range, offset_range)
            y_random = y + random.randint(-offset_range, offset_range)

            ball_radius = 10  # Raio fixo ou aleatório, se preferir

            # Obtém a densidade da bola do slider
            current_ball_density = ball_density_slider.get_current_value()

            print("Ball density", current_ball_density)

            new_ball = Ball(ball_radius, current_ball_density, (x_random, height - y_random))
            balls.append(new_ball)

        manager.process_events(event)

    # Atualiza o valor da altura e densidade do fluido com os sliders
    fluid_height = fluid_height_slider.get_current_value()
    fluid_density = fluid_density_slider.get_current_value()
    print(f"Fluid density {fluid_density}, Ball density {current_ball_density}")



    # Aplica a flutuação em cada bola e desenha as bolas
    mouse_pos = pygame.mouse.get_pos()
    tooltip_text = ''
    for ball in balls:
        ball.apply_buoyancy(fluid_height, fluid_density)
        ball.apply_arrastro(fluid_height)
        ball.draw(window)
        if ball.is_mouse_over(mouse_pos):
            tooltip_text = f'Density: {ball.mass:.2f}'
            break

    tooltip.set_text(tooltip_text)

    # Desenha o nível do fluido
    draw_fluid_line(window, fluid_height)

    # Atualiza o GUI
    manager.update(time_delta)

    # Atualiza o espaço de física
    space.step(1 / 60.0)

    # Desenha a interface
    manager.draw_ui(window)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
