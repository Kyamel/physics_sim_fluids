# model/box.py
# modelo de um box pymunk

from typing import Tuple
import pymunk
from model.interface import ShapeInterface

class Box(ShapeInterface):
    def __init__(self, size: Tuple[float, float], radius: float = 0) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly.create_box(self.body, size, radius)

    def set_friction(self, value: float) -> None:
        self.shape.friction = value

    def set_elasticity(self, value: float) -> None:
        self.shape.elasticity = value

    def set_collision_type(self, collision_type: int) -> None:
        self.shape.collision_type = collision_type

    def set_sensor(self, is_sensor: bool) -> None:
        self.shape.sensor = is_sensor

    def apply_force(self, force: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        pass  # Caixas estáticas não têm força aplicada

    def apply_impulse(self, impulse: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        pass  # Caixas estáticas não têm impulso aplicado

    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        pass  # Caixas estáticas não têm velocidade

    def set_angular_velocity(self, angular_velocity: float) -> None:
        pass  # Caixas estáticas não têm velocidade angular