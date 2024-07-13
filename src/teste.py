# main.py

from typing import List
import pygame
import pymunk
import random
from model.drawable.particle import DrawableParticle
from model.drawable.segment import DrawableSegment
from utils import values

def main():
    # Inicialização do Pygame
    pygame.init()
    screen = pygame.display.set_mode((values.WIDTH, values.HEIGHT))
    pygame.display.set_caption("Simulador de Fluidos 2D com pymunk")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)  # Fonte para exibir o FPS

    # Configuração do Pymunk
    space = pymunk.Space()
    space.gravity = (0, -values.GRAVITY)  # Gravidade negativa para baixo

    # Adicionar o "chão" como uma linha estática
    ground = DrawableSegment((0, 0), (values.WIDTH, 0), 5)
    ground.set_friction(0.5)
    space.add(ground.body, ground.shape)

    # Adicionar paredes laterais como linhas estáticas
    left_wall = DrawableSegment((0, 0), (0, values.HEIGHT), 5)
    right_wall = DrawableSegment((values.WIDTH, 0), (values.WIDTH, values.HEIGHT), 5)
    left_wall.set_friction(0.5)
    right_wall.set_friction(0.5)
    space.add(left_wall.body, right_wall.body, left_wall.shape, right_wall.shape)

    # Cria uma rampa estática (segmento inclinado)
    ramp = DrawableSegment((50, 300), (300, 500), 5)
    ramp.set_friction(1.0)
    space.add(ramp.body, ramp.shape)

    # Cria uma superficie quadrada
    square_shape1 = DrawableSegment((30,20), (30,100),5)
    square_shape2 = DrawableSegment((30,20),(110,20),5)
    square_shape3 = DrawableSegment((110,20), (110,100),5)
    space.add(square_shape1.body,square_shape1.shape,square_shape2.body,square_shape2.shape,square_shape3.body,square_shape3.shape)

    # Função para adicionar partículas
    def add_particle(x, y) -> DrawableParticle:
        x = random.uniform(x-0.1, x+0.1)
        y = random.uniform(y-0.1, y+0.1)
        particle = DrawableParticle(x, y, 5)  # Raio 5 para a partícula
        particle.set_elasticity(0.5)
        particle.set_friction(0.5)
        space.add(particle.body, particle.shape)
        return particle

    # Lista de partículas
    particles: List[DrawableParticle] = []

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
            particle.draw(screen)

        # Desenhar o "chão"
        ground.draw(screen)
        # Desenhar paredes (linhas estáticas)
        left_wall.draw(screen)
        right_wall.draw(screen)
        # Desenhar a rampa
        ramp.draw(screen)
        
        #desenhando a superficie quadrada
        square_shape1.draw(screen)
        square_shape2.draw(screen)
        square_shape3.draw(screen)
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
