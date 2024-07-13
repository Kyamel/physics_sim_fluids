import pygame
from typing import Tuple

import pymunk
from model.particle import Particle
from utils import values

class DrawableParticle(Particle):
    def __init__(self, x, y, radius: float, mass=1.0, raio_externo = 0, raio_interno = 5, color: Tuple[int, int, int] = values.PARTICLE_COLOR):
        self.color = color
        super().__init__(x, y, radius, mass, raio_externo, raio_interno)

    def draw(self, screen: pygame.Surface) -> None:
        pos_x = int(self.body.position.x)
        pos_y = int(values.HEIGHT - self.body.position.y)
        pygame.draw.circle(screen, self.color, (pos_x, pos_y), self.shape.radius*2)

    def add_to_space(self, space: pymunk.Space) -> None:
        super().add_to_space(space)

    def set_color(self, color: Tuple[int, int, int]):
        self.color = color