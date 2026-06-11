
import pygame

from DataClasses.ControlData import ControlType
from Model.Score.ScoreControl import ScoreControl


class TextItem(ScoreControl):

    def __init__(self, rect, text, main_screen, parent_container, font_size=20):
        super().__init__(rect, control_type=ControlType.TEXT, name="TextItem", parent=parent_container)
        self.font = pygame.font.SysFont("segoeui", font_size, bold=True)
        self.rect = rect
        self.text = text
        self.main_screen = main_screen
        self.parent_container = parent_container
        self.color = (120,190,255)

    def set_app_state(self, app_state):
         self.app_state = app_state

    def draw(self, scrollable_screen=None):

        if scrollable_screen is None:
            scrollable_screen = self.main_screen

        r = self.rect.move(
            0,
            -self.parent_container.scroll_y
        )

        pygame.draw.rect(
            scrollable_screen,
            self.color,
            r,
            border_radius=6
        )

        pygame.draw.rect(
            scrollable_screen,
            (30, 30, 30),
            r,
            2,
            border_radius=6
        )

        txt = self.font.render(
            self.text,
            True,
            (0, 0, 0)
        )

        scrollable_screen.blit(
            txt,
            (
                r.x + 10,
                r.y + 15
            )
        )

    