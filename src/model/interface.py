from abc import ABC, abstractmethod
from typing import Tuple

class ShapeInterface(ABC):
    @abstractmethod
    def set_friction(self, value: float) -> None:
        pass

    @abstractmethod
    def set_elasticity(self, value: float) -> None:
        pass

    @abstractmethod
    def set_collision_type(self, collision_type: int) -> None:
        pass

    @abstractmethod
    def set_sensor(self, is_sensor: bool) -> None:
        pass

    @abstractmethod
    def apply_force(self, force: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        pass

    @abstractmethod
    def apply_impulse(self, impulse: Tuple[float, float], point: Tuple[float, float] = (0, 0)) -> None:
        pass

    @abstractmethod
    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        pass

    @abstractmethod
    def set_angular_velocity(self, angular_velocity: float) -> None:
        pass
