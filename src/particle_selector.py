import pygame
import pymunk
from typing import List
from model.drawable.particle import DrawableParticle
from model.drawable.segment import DrawableSegment
from utils import values
from visual.renderer import Renderer
from visual.sidebar import Sidebar


def main():
    # Configura o pygame
    pygame.init()
    screen = pygame.display.set_mode((values.WIDTH, values.HEIGHT))

    # Configura a barra lateral
    sidebar = Sidebar((values.WIDTH, values.HEIGHT))

    # Configura o espaço físico pymunk
    space = pymunk.Space()
    space.gravity = (0, -values.GRAVITY)

    #Configura o renderizador
    renderer = Renderer(screen, space, sidebar)

    # Adiciona o chão como uma linha estática
    ground = DrawableSegment((0, 0), (values.WIDTH, 0), 5)
    ground.set_friction(0.5)
    ground.add_to_space(space)

    # Adiciona paredes laterais como linhas estáticas
    left_wall = DrawableSegment((0, 0), (0, values.HEIGHT), 5)
    right_wall = DrawableSegment((values.WIDTH, 0), (values.WIDTH, values.HEIGHT), 5)
    left_wall.set_friction(0.5)
    left_wall.add_to_space(space)
    right_wall.set_friction(0.5)
    right_wall.add_to_space(space)

    # Cria uma superficie quadrada
    square_shape1 = DrawableSegment((30,20), (30,100),5)
    square_shape1.add_to_space(space)
    square_shape2 = DrawableSegment((30,20),(110,20),5)
    square_shape2.add_to_space(space)
    square_shape3 = DrawableSegment((110,20), (110,100),5)
    square_shape3.add_to_space(space)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not sidebar.menu_button.relative_rect.collidepoint(event.pos) and not sidebar.menu_panel.relative_rect.collidepoint(event.pos):
                    x, y = pygame.mouse.get_pos()
                    mass = float(sidebar.mass_input.get_text())
                    inertia = float(sidebar.inertia_input.get_text())
                    renderer.add_particle(x, y, mass, inertia)
                    
            renderer.sidebar.handle_events(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            x, y = pygame.mouse.get_pos()
            mass = float(sidebar.mass_input.get_text())
            inertia = float(sidebar.inertia_input.get_text())
            renderer.add_particle(x, y, mass, inertia)

        renderer.update()
        renderer.draw_particles()
        renderer.show_statistics()   

        ground.draw(screen)
        left_wall.draw(screen)
        right_wall.draw(screen)
        square_shape1.draw(screen)
        square_shape2.draw(screen)
        square_shape3.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()