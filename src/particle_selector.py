import pygame
import pygame_gui
import pymunk
import random
from typing import List
from model.drawable.particle import DrawableParticle
from model.drawable.segment import DrawableSegment
from utils import values

# Variável global para armazenar o tipo de partícula selecionada
selected_particle_type = 1  # Inicialmente seleciona o tipo 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((values.WIDTH, values.HEIGHT))
    pygame.display.set_caption("Simulador de Fluidos 2D com pymunk")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    manager = pygame_gui.UIManager((values.WIDTH, values.HEIGHT))

    menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((values.WIDTH - 100, 10), (90, 40)), text='Menu', manager=manager)

    menu_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((values.WIDTH, 0), (300, values.HEIGHT)), manager=manager)

    # Inputs do menu
    mass_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (280, 30)), manager=manager, container=menu_panel)
    mass_input.set_text('1.0')

    inertia_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 90), (280, 30)), manager=manager, container=menu_panel)
    inertia_input.set_text('10.0')

    color_picker = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 130), (280, 40)), text='Escolher Cor', manager=manager, container=menu_panel)

    # Seletor para escolher o tipo de partícula
    particle_selector = pygame_gui.elements.UIDropDownMenu(['1', '2', '3'],starting_option='1',relative_rect=pygame.Rect((10, 170), (280, 30)), manager=manager, container=menu_panel)

    def add_particle(x, y, mass, inertia):
        x = random.uniform(x - 0.1, x + 0.1)
        y = random.uniform(y - 0.1, y + 0.1)
        
        if selected_particle_type == 1:
            particle = DrawableParticle(x, y, 5, mass, color=(0, 255, 0))
        elif selected_particle_type == 2:
            particle = DrawableParticle(x, y, 5, mass * 2, color=(255, 0, 0))  # Exemplo de atributos diferentes
        elif selected_particle_type == 3:
            particle = DrawableParticle(x, y, 5, mass * 0.5, color=(0, 0, 255))  # Exemplo de atributos diferentes
        else:
            particle = DrawableParticle(x, y, 5, mass, inertia, values.PARTICLE_COLOR)  # Fallback para tipo 1 por padrão
        
        particle.set_elasticity(0.5)
        particle.set_friction(0.5)
        space.add(particle.body, particle.shape)
        return particle

    # Configuração do Pymunk
    space = pymunk.Space()
    space.gravity = (0, -values.GRAVITY)

    # Adicionar o "chão" como uma linha estática
    ground = DrawableSegment((0, 0), (values.WIDTH, 0), 5)
    ground.set_friction(0.5)
    ground.add_to_space(space)

    # Adicionar paredes laterais como linhas estáticas
    left_wall = DrawableSegment((0, 0), (0, values.HEIGHT), 5)
    right_wall = DrawableSegment((values.WIDTH, 0), (values.WIDTH, values.HEIGHT), 5)
    left_wall.add_to_space(space)
    left_wall.set_friction(0.5)
    right_wall.set_friction(0.5)
    right_wall.add_to_space(space)

    # Cria uma rampa estática (segmento inclinado)
    ramp = DrawableSegment((50, 100), (300, 200), 5)
    ramp.set_friction(1.0)
    ramp.add_to_space(space)

    # Lista de partículas
    particles: List[DrawableParticle] = []

    # Loop principal
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_panel.relative_rect.collidepoint(event.pos):
                    pass
                else:
                    x, y = event.pos
                    mass = float(mass_input.get_text())
                    inertia = float(inertia_input.get_text())
                    particle = add_particle(x, y, mass, inertia)
                    particles.append(particle)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if menu_panel.relative_rect.x == values.WIDTH:
                    menu_panel.set_relative_position((values.WIDTH - 300, 0))
                else:
                    menu_panel.set_relative_position((values.WIDTH, 0))

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == particle_selector:
                    selected_index = event.text  # Extrai o número do tipo de partícula
                    global selected_particle_type
                    selected_particle_type = int(selected_index)

            manager.process_events(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            x, y = pygame.mouse.get_pos()
            mass = float(mass_input.get_text())
            inertia = float(inertia_input.get_text())
            particle = add_particle(x, y, mass, inertia)
            particles.append(particle)

        screen.fill(values.BACKGROUND_COLOR)

        # Simulação física
        space.step(1 / 60.0)

        # Desenhar partículas
        for particle in particles:
            particle.draw(screen)

        # Desenhar o "chão"
        ground.draw(screen)
        # Desenhar paredes (linhas estáticas)
        left_wall.draw(screen)
        right_wall.draw(screen)
        # Desenhar a rampa
        ramp.draw(screen)

        # Calcular e exibir o FPS
        fps = clock.get_fps()
        fps_text = font.render(f" FPS: {int(fps)}", True, values.TEXT_COLOR)
        particle_count = font.render(f" Particle Count: {len(particles)}", True, values.TEXT_COLOR)
        screen.blit(particle_count, (10, 30))
        screen.blit(fps_text, (10, 10))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
