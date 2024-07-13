import pygame
from typing import Tuple
from model.particle import Particle
from utils import values

class DrawableParticle(Particle):
    def __init__(self, x: float, y: float, radius: float, mass=1.0, moment=10.0):
        super().__init__(x, y, radius, mass, moment)

    def draw(self, screen: pygame.Surface) -> None:
        pos_x = int((self.body.position.x))
        pos_y = int((values.HEIGHT - self.body.position.y))
        pygame.draw.circle(screen, values.PARTICLE_COLOR, (pos_x, pos_y), self.shape.radius * 2)

 