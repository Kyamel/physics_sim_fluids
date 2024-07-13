from typing import Tuple
import pymunk
from model.interface import ShapeInterface

class Segment(ShapeInterface):
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float], radius: float = 5):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, a, b, radius)

    def add_to_space(self, space: pymunk.Space) -> None:
        space.add(self.body, self.shape)

    def set_friction(self, value: float) -> None:
        self.shape.friction = value

    def set_elasticity(self, value: float) -> None:
        self.shape.elasticity = value

    def set_collision_type(self, collision_type: int) -> None:
        self.shape.collision_type = collision_type

    def set_sensor(self, is_sensor: bool) -> None:
        self.shape.sensor = is_sensor

    def apply_force(self, force: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        pass  # Segmentos estáticos não têm força aplicada

    def apply_impulse(self, impulse: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        pass  # Segmentos estáticos não têm impulso aplicado

    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        pass  # Segmentos estáticos não têm velocidade

    def set_angular_velocity(self, angular_velocity: float) -> None:
        pass  # Segmentos estáticos não têm velocidade angular