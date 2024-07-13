import pygame
from typing import Sequence, Tuple

import pymunk
from model.poly import Poly
from utils import values

class DrawablePoly(Poly):
    def __init__(self, vertices: Sequence[Tuple[float, float]]) -> None:
        super().__init__(vertices)
    
    def draw(self, screen: pygame.Surface)-> None:
        points = []
        for v in self.vertices:
            points = (v.rotated(self.body.angle)+self.body.position)
        for p in points:
            points = (p.x, 300 - p.y)
        pygame.draw.polygon(screen,values.LINE_COLOR,points)
    
    def add_to_space(self, space: pymunk.Space) -> None:
        super().add_to_space(space)