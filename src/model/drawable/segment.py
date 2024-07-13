import pymunk
import pygame
from typing import Tuple
from model.segment import Segment
from utils import values

class DrawableSegment(Segment):
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float], radius: float = 5):
        super().__init__(a, b, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.line(screen, values.LINE_COLOR, self.shape.a, (self.shape.b[0], values.HEIGHT - self.shape.b[1]), self.shape.radius)
