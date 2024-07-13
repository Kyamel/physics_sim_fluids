# visual/renderer.py

import pygame
from model.particle import Particle
from model.segment import Segment
from utils import values

class Renderer:
    def __init__(self, screen) -> None:
        self.screen = screen

    def draw_particle(self, particle: Particle) -> None:
        pos_x = int(particle.body.position.x)
        pos_y = int(values.HEIGHT - particle.body.position.y)
        pygame.draw.circle(self.screen, values.PARTICLE_COLOR, (pos_x, pos_y), 10)

    def draw_segment(self, segment: Segment) -> None:
        segment.shape.a.y = -segment.shape.y
        segment.shape.b.y = -segment.shape.y
        pygame.draw.line(self.screen, values.LINE_COLOR, segment.shape.a, segment.shape.b, 5)
