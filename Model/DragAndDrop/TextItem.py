
import pygame

from DataClasses.ControlData import ControlType
from Model.Score.ScoreControl import ScoreControl


class TextItem(ScoreControl):

    def __init__(self, rect, text, parent_container, 
                 font_size=20, bg_color=(120,190,255), text_color=(20,20,20),
                 border_color=(200,200,200), border_tickness=2):
        super().__init__(rect, control_type=ControlType.TEXT, name="TextItem", parent=parent_container)
        self.font = pygame.font.SysFont("segoeui", font_size, bold=True)
        self.rect = rect
        self.text = text
        self.parent_container = parent_container
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_tickness = border_tickness
        self.border_color = border_color

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
            self.bg_color,
            r,
            border_radius=2
        )

        pygame.draw.rect(
            scrollable_screen,
            self.border_color,
            r,
            self.border_tickness,
            border_radius=2
        )

        txt = self.font.render(
            self.text,
            True,
            self.text_color
        )

        scrollable_screen.blit(
            txt,
            (
                r.x + 10,
                r.y + 15
            )
        )

    