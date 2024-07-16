# src\view\sidebar.py
# menu lateral

import pygame
import pygame_gui
from utils import values
from view.menu import MenuInterface

class Sidebar(MenuInterface):
    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.selected_particle_type = 1  # Inicialmente seleciona o tipo 1
        self.manager = pygame_gui.UIManager(screen_size)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_size[0] - 100, 10), (90, 40)),
            text='Menu',
            manager=self.manager
        )
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((screen_size[0], 0), (300, screen_size[1])),
            manager=self.manager
        )
        self.mass_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 50), (280, 30)),
            manager=self.manager,
            container=self.menu_panel
        )
        self.mass_input.set_text('1.0')

        self.inertia_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 90), (280, 30)),
            manager=self.manager,
            container=self.menu_panel
        )
        self.inertia_input.set_text('10.0')

        self.color_picker = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 130), (280, 40)),
            text='Escolher Cor',
            manager=self.manager,
            container=self.menu_panel
        )

        self.particle_selector = pygame_gui.elements.UIDropDownMenu(
            ['1', '2', '3'], starting_option='1',
            relative_rect=pygame.Rect((10, 170), (280, 30)),
            manager=self.manager,
            container=self.menu_panel
        )

        self.selected_color = (0, 255, 0)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_button.relative_rect.collidepoint(event.pos):
                if self.menu_panel.relative_rect.x == values.WIDTH:
                    self.menu_panel.set_relative_position((values.WIDTH - 300, 0))
                    self.menu_button.set_relative_position((values.WIDTH - 400, 10))
                    self.menu_button.set_text('X')
                else:
                    self.menu_panel.set_relative_position((values.WIDTH, 0))
                    self.menu_button.set_relative_position((values.WIDTH - 100, 10))
                    self.menu_button.set_text('Menu')
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.particle_selector:
                self.selected_particle_type = int(event.text)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.color_picker:
                self.selected_color = pygame.color.THECOLORS['blue']  # Temporarily set to blue

        self.manager.process_events(event)

    def update(self, time_delta: float) -> None:
        self.manager.update(time_delta)

    def draw(self, screen: pygame.Surface) -> None:
        self.manager.draw_ui(screen)