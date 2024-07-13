from typing import Tuple
import pymunk
from model.interface import ShapeInterface


class Particle(ShapeInterface):
    def __init__(self, x, y, radius: float, mass=1.0, moment=10.0) -> None:
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)

    def set_friction(self, value: float) -> None:
        self.shape.friction = value

    def set_elasticity(self, value: float) -> None:
        self.shape.elasticity = value

    def set_collision_type(self, collision_type: int) -> None:
        self.shape.collision_type = collision_type

    def set_sensor(self, is_sensor: bool) -> None:
        self.shape.sensor = is_sensor

    def apply_force(self, force: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        self.body.apply_force_at_local_point(force, point)

    def apply_impulse(self, impulse: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        self.body.apply_impulse_at_local_point(impulse, point)

    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        self.body.velocity = velocity

    def set_angular_velocity(self, angular_velocity: float) -> None:
        self.body.angular_velocity = angular_velocity



