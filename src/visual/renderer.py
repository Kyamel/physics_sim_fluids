# visual/renderer.py
import random
from typing import List
import pygame
import pymunk
from model.drawable.particle import DrawableParticle
from model.particle import Particle
from model.segment import Segment
from utils import values
from visual import sidebar

class Renderer:
    def __init__(self, screen: pygame.Surface, space: pymunk.Space, sidebar: sidebar.Sidebar) -> None:
        self.screen = screen
        self.space = space
        self.sidebar = sidebar
        self.particles: List[DrawableParticle] = []
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(60) / 1000.0
        pygame.display.set_caption("Simulador de Fluidos 2D com pymunk")
        self.font = pygame.font.Font(None, 30)

    def add_particle(self, x: int, y: int, mass: float, inertia: float) -> Particle:
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)
        color = self.sidebar.selected_color

        if self.sidebar.selected_particle_type == 1:
            particle = DrawableParticle(x, y, 5, mass, color=(255, 0, 0))
        elif self.sidebar.selected_particle_type == 2:
            particle = DrawableParticle(x, y, 5, mass * 2, color=(0, 255, 0))
        elif self.sidebar.selected_particle_type == 3:
            particle = DrawableParticle(x, y, 5, mass * 0.5, color=(0, 0, 255))
        else:
            particle = DrawableParticle(x, y, 5, mass, inertia, values.PARTICLE_COLOR)
        
        particle.set_elasticity(0.5)
        particle.set_friction(0.5)
        self.space.add(particle.body, particle.shape)
        self.particles.append(particle)
        return particle
    
    def update(self) -> None:
        self.screen.fill(values.BACKGROUND_COLOR)
        self.time_delta = self.clock.tick(60) / 1000.0
        self.space.step(1 / 60.0)
        self.sidebar.update(self.time_delta)
        self.sidebar.draw(self.screen)


    def show_statistics(self) -> None:
        fps = self.clock.get_fps()
        fps_text = self.font.render(f" FPS: {int(fps)}", True, values.TEXT_COLOR)
        particle_count = self.font.render(f" Particle Count: {len(self.particles)}", True, values.TEXT_COLOR)
        self.screen.blit(particle_count, (10, 30))
        self.screen.blit(fps_text, (10, 10))

    def draw_particles(self) -> None:
        for particle in self.particles:
            particle.draw(self.screen)
