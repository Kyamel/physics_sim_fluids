import pygame
import pymunk
import random
from typing import List
from model.drawable.particle import DrawableParticle
from model.drawable.segment import DrawableSegment
from utils import values
from visual.sidebar import Sidebar


def main():
    pygame.init()
    screen = pygame.display.set_mode((values.WIDTH, values.HEIGHT))
    pygame.display.set_caption("Simulador de Fluidos 2D com pymunk")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    sidebar = Sidebar((values.WIDTH, values.HEIGHT))

    def add_particle(x, y, mass, inertia):
        x = random.uniform(x - 0.1, x + 0.1)
        y = random.uniform(y - 0.1, y + 0.1)
        
        if sidebar.selected_particle_type == 1:
            # Partícula de água
            particle = DrawableParticle(x, y, 5, mass, color=(0, 0, 255))  # Azul
            particle.shape.filter = pymunk.ShapeFilter(categories=0b1, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b10)
        elif sidebar.selected_particle_type == 2:
            # Partícula de óleo
            particle = DrawableParticle(x, y, 5, mass * 2, color=(255, 0, 0))  # Vermelho
            particle.shape.filter = pymunk.ShapeFilter(categories=0b10, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1)
        else:
            particle = DrawableParticle(x, y, 5, mass, inertia, values.PARTICLE_COLOR)
        
        particle.set_elasticity(0.5)
        particle.set_friction(0.5)
        space.add(particle.body, particle.shape)
        return particle

    space = pymunk.Space()
    space.gravity = (0, -values.GRAVITY)

    ground = DrawableSegment((0, 0), (values.WIDTH, 0), 5)
    ground.set_friction(0.5)
    ground.add_to_space(space)

    left_wall = DrawableSegment((0, 0), (0, values.HEIGHT), 5)
    right_wall = DrawableSegment((values.WIDTH, 0), (values.WIDTH, values.HEIGHT), 5)
    left_wall.add_to_space(space)
    left_wall.set_friction(0.5)
    right_wall.set_friction(0.5)
    right_wall.add_to_space(space)

   # Cria uma superficie quadrada
    square_shape1 = DrawableSegment((30,20), (30,100),5)
    square_shape1.add_to_space(space)
    square_shape2 = DrawableSegment((30,20),(110,20),5)
    square_shape2.add_to_space(space)
    square_shape3 = DrawableSegment((110,20), (110,100),5)
    square_shape3.add_to_space(space)

    particles: List[DrawableParticle] = []

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not sidebar.menu_button.relative_rect.collidepoint(event.pos) and not sidebar.menu_panel.relative_rect.collidepoint(event.pos):
                    x, y = pygame.mouse.get_pos()
                    mass = float(sidebar.mass_input.get_text())
                    inertia = float(sidebar.inertia_input.get_text())
                    particle = add_particle(x, y, mass, inertia)
                    particles.append(particle)

            sidebar.process_events(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            x, y = pygame.mouse.get_pos()
            mass = float(sidebar.mass_input.get_text())
            inertia = float(sidebar.inertia_input.get_text())
            particle = add_particle(x, y, mass, inertia)
            particles.append(particle)

        screen.fill(values.BACKGROUND_COLOR)
        space.step(1 / 60.0)

        for particle in particles:
            if particle.shape.filter.categories == 0b10:  # Partícula de óleo
                # Adiciona uma força adicional para simular a densidade
                particle.body.apply_force_at_local_point((0, -50), (0, 0))

            particle.draw(screen)

        ground.draw(screen)
        left_wall.draw(screen)
        right_wall.draw(screen)
        square_shape1.draw(screen)
        square_shape2.draw(screen)
        square_shape3.draw(screen)

        fps = clock.get_fps()
        fps_text = font.render(f" FPS: {int(fps)}", True, values.TEXT_COLOR)
        particle_count = font.render(f" Particle Count: {len(particles)}", True, values.TEXT_COLOR)
        screen.blit(particle_count, (10, 30))
        screen.blit(fps_text, (10, 10))

        sidebar.update(time_delta)
        sidebar.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()