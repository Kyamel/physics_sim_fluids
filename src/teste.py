# main.py

from typing import List
import pygame
import pymunk
import random
from model.particle import Particle
from model.segment import Segment
from visual.renderer import Renderer
from utils import values

def main():
    # Inicialização do Pygame
    pygame.init()
    screen = pygame.display.set_mode((values.WIDTH, values.HEIGHT))
    pygame.display.set_caption("Simulador de Fluidos 2D com pymunk")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)  # Fonte para exibir o FPS

    # valesuração do Pymunk
    space = pymunk.Space()
    space.gravity = (0, -values.GRAVITY)  # Gravidade negativa para baixo

    # Inicializar Renderer
    renderer = Renderer(screen)

    # Adicionar o "chão" como uma linha estática
    ground = Segment((0, 0), (values.WIDTH, 0), 5)
    ground.set_friction(0.5)
    space.add(ground.body, ground.shape)

    # Adicionar paredes laterais como linhas estáticas
    left_wall = Segment((0, 0), (0, values.HEIGHT), 5)
    right_wall = Segment((values.WIDTH, 0), (values.WIDTH, values.HEIGHT), 5)
    left_wall.set_friction(0.5)
    right_wall.set_friction(0.5)
    space.add(left_wall.body, right_wall.body, left_wall.shape, right_wall.shape)

    # Cria uma rampa estática (segmento inclinado)
    ramp = Segment((50, 100), (300, 200), 5)
    ramp.set_friction(1.0)
    space.add(ramp.body, ramp.shape)

    # Função para adicionar partículas
    def add_particle(x, y) -> Particle:
        x = random.uniform(x-0.1, x+0.1)
        y = random.uniform(y-0.1, y+0.1)
        particle = Particle(x, y, 5)  # Raio 5 para a partícula
        particle.set_elasticity(0.5)
        particle.set_friction(0.5)
        space.add(particle.body, particle.shape)
        return particle

    # Lista de partículas
    particles: List[Particle] = []

    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                particle = add_particle(x, y)
                particles.append(particle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            x, y = pygame.mouse.get_pos()
            particle = add_particle(x, y)
            particles.append(particle)

        screen.fill(values.BACKGROUND_COLOR)

        # Simulação física
        space.step(1 / 60.0)

        # Desenhar partículas
        for particle in particles:
            renderer.draw_particle(particle)

        # Desenhar o "chão"
        renderer.draw_segment(ground)
        # Desenhar paredes (linhas estáticas)
        renderer.draw_segment(left_wall)
        renderer.draw_segment(right_wall)
        # Desenhar a rampa
        renderer.draw_segment(ramp)

        # Calcular e exibir o FPS
        fps = clock.get_fps()
        fps_text = font.render(f" FPS: {int(fps)}", True, values.TEXT_COLOR)
        particle_count = font.render(f" Particle Count: {len(particles)}", True, values.TEXT_COLOR)
        screen.blit(particle_count, (10, 30))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
