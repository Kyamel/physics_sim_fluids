from abc import ABC, abstractmethod
import pygame

class MenuInterface(ABC):
    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        pass
    
    @abstractmethod
    def update(self, time_delta: float) -> None:
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass
