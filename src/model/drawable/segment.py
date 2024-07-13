import pymunk
import pygame
from typing import Tuple
from model.segment import Segment
from utils import values

class DrawableSegment(Segment):
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float], radius: float = 5):
        super().__init__(a, b, radius)

    def draw(self, screen: pygame.Surface) -> None:
        start = self.shape.a.x, values.HEIGHT -self.shape.a.y
        end = self.shape.b.x, values.HEIGHT -self.shape.b.y
        pygame.draw.line(screen, values.LINE_COLOR, start, end, int(self.shape.radius))