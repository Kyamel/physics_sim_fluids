import random
import time
from typing import List, Tuple
import pygame
import pymunk
import pygame_gui

# Inicializa o pygame e pymunk
pygame.init()

# Parâmetros da janela
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Criação do espaço de física do pymunk
SPACE = pymunk.Space()
SPACE.gravity = (0, -980)  # Gravidade padrão

# Inicializa o pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Função para arredondar valores ao passo desejado
def round_to_step(value, step):
    return round(value / step) * step

# Classe para gerenciar a interface do usuário
class GUI:
    def __init__(self):

        self.fluid_density_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 40), (200, 25)),
            start_value=1.0,
            value_range=(1.0, 10.0),
            manager=manager
        )

        self.fluid_density_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 20), (200, 25)),
            text=f"Fluid Density: {self.fluid_density_slider.get_current_value():.1f}",
            manager=manager
        )
        self.ball_density_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 90), (200, 25)),
            start_value=5.0,
            value_range=(1.0, 10.0),
            manager=manager
        )

        self.ball_density_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 70), (200, 25)),
            text=f"New Ball Density: {self.ball_density_slider.get_current_value():.1f}",
            manager=manager
        )

        self.tooltip = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (100, 30)),
            text='',
            manager=manager
        )

        self.fluid_height = int(HEIGHT // 2)

    def process_events(self, event):
        # Processa eventos da interface
        manager.process_events(event)

    def update(self, time_delta):
        self.fluid_density_label.set_text(f"Fluid Density: {self.get_fluid_density():}")
        self.ball_density_label.set_text(f"New Ball Density: {self.get_ball_density():}")
        manager.update(time_delta)

    def draw(self, screen):
        manager.draw_ui(screen)

    def increment_fluid_height(self, increment: int):
        self.fluid_height += increment

    def get_fluid_height(self):
        return self.fluid_height

    def get_fluid_density(self):
        return round_to_step(self.fluid_density_slider.get_current_value(), 1)

    def get_ball_density(self):
        return round_to_step(self.ball_density_slider.get_current_value(), 1)

    def set_tooltip_text(self, text: str):
        self.tooltip.set_text(text)

# Classe para gerenciar o comportamento das bolas
class Ball:
    def __init__(self, radius: float, mass: float, position: Tuple[int, int], color=(255, 255, 255)):
        self.mass = mass
        self.radius = radius
        self.color = color
        self.body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, radius))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.5
        self.body.angular_velocity = 0
        self.body.moment = float("inf")  # Impede a rotação
        SPACE.add(self.body, self.shape)
        self.has_incremented = False

    def check_increment_water(self, fluid_height):
        if not self.has_incremented and self.body.position.y <= fluid_height:
            self.has_incremented = True
            return True
        return False

    def draw(self, screen: pygame.Surface):
        pos_x = int(self.body.position.x)
        pos_y = int(HEIGHT - self.body.position.y)
        pygame.draw.circle(screen, self.color, (pos_x, pos_y), int(self.shape.radius))

    def empuxo(self, fluid_height: int, fluid_density: float = 1.0, gravity: float = -980):
        submersion_depth = max(0, fluid_height - self.body.position.y)
        if submersion_depth > 0:
            buoyancy_force = fluid_density * gravity * 1
            self.body.apply_force_at_local_point((0, -buoyancy_force))

    def arrastro(self, fluid_height: int, drag_coefficient: float = 1.0):
        submersion_depth = fluid_height - self.body.position.y
        if submersion_depth >= 0:
            drag_force_y = -drag_coefficient * self.body.velocity.y
            drag_force_x = -drag_coefficient * self.body.velocity.x
            self.body.apply_force_at_local_point((drag_force_x * 20, drag_force_y * 100))

    def is_mouse_over(self, mouse_pos: Tuple[int, int]) -> bool:
        ball_pos = (int(self.body.position.x), int(HEIGHT - self.body.position.y))
        distance = ((mouse_pos[0] - ball_pos[0]) ** 2 + (mouse_pos[1] - ball_pos[1]) ** 2) ** 0.5
        return distance <= self.radius

# Classe para gerenciar a simulação
class Simulation:
    def __init__(self):
        self.balls: List[Ball] = []

    def create_ball(self, x, y, density):
        offset_range = 2
        x_random = x + random.randint(-offset_range, offset_range)
        y_random = y + random.randint(-offset_range, offset_range)

        
        new_ball = Ball(10, density, (x_random, HEIGHT - y_random), (255*(density/10), 255*(density/10), 255))
        self.balls.append(new_ball)

    def update_balls(self, fluid_height, fluid_density, gui):
        for ball in self.balls:
            ball.empuxo(fluid_height, fluid_density)
            ball.arrastro(fluid_height)
            if ball.check_increment_water(gui.get_fluid_height()):
                gui.increment_fluid_height(1)

    def draw_balls(self, screen, mouse_pos, gui):
        tooltip_text = ''
        for ball in self.balls:
            if ball.is_mouse_over(mouse_pos):
                tooltip_text = f'Density: {ball.mass:.2f}'
            ball.draw(screen)
        gui.set_tooltip_text(tooltip_text)

# Função para criar paredes no pymunk
def create_walls():
    wall_thickness = 1
    walls = [
        pymunk.Segment(SPACE.static_body, (0, HEIGHT - wall_thickness), (WIDTH, HEIGHT - wall_thickness), wall_thickness),
        pymunk.Segment(SPACE.static_body, (0, wall_thickness), (WIDTH, wall_thickness), wall_thickness),
        pymunk.Segment(SPACE.static_body, (wall_thickness, 0), (wall_thickness, HEIGHT), wall_thickness),
        pymunk.Segment(SPACE.static_body, (WIDTH - wall_thickness, 0), (WIDTH - wall_thickness, HEIGHT), wall_thickness)
    ]
    for wall in walls:
        wall.friction = 1.0
        wall.elasticity = 0.8
        SPACE.add(wall)

# Função para desenhar o nível do fluido
def draw_fluid_area(screen, fluid_height):
    water_color = (0, 0, 255, 100)  # Azul com transparência
    water_surface = pygame.Surface((WIDTH, fluid_height), pygame.SRCALPHA)  # Superfície transparente com altura = fluid_height
    pygame.draw.rect(water_surface, water_color, pygame.Rect(0, 0, WIDTH, fluid_height))
    screen.blit(water_surface, (0, HEIGHT - fluid_height))  # Desenha a água de baixo para cima


# Inicializa a simulação
create_walls()
gui = GUI()
simulation = Simulation()

# Loop principal
running = True
while running:
    time_delta = CLOCK.tick(60) / 1000.0
    WINDOW.fill((0, 0, 0))

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = pygame.mouse.get_pos()
            ball_density = gui.get_ball_density()
            simulation.create_ball(x, y, ball_density)


        gui.process_events(event)

    # Atualiza os valores da interface
    #fluid_height = gui.get_fluid_height()
    fluid_density = gui.get_fluid_density()

    # Atualiza a simulação
    simulation.update_balls(gui.get_fluid_height(), fluid_density, gui)

    # Desenha os elementos
    draw_fluid_area(WINDOW, gui.get_fluid_height())
    simulation.draw_balls(WINDOW, pygame.mouse.get_pos(), gui)

    # Atualiza e desenha a interface
    gui.update(time_delta)
    gui.draw(WINDOW)

    # Atualiza o espaço de física
    SPACE.step(1 / 60.0)

    pygame.display.flip()

pygame.quit()
