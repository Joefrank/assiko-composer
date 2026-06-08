import pygame

from DataClasses.ControlData import ControlType
from Model.Control import Control


class ScorePage(Control):

    def __init__(self, rect, page_number, main_screen, font, parent_container, show_page_number=True):
        super().__init__(rect, ControlType.CONTAINER, f"Score Page {page_number}")
        self.number = page_number
        self.main_screen = main_screen
        self.font = font
        self.show_page_number = show_page_number
        self.parent_container = parent_container    

    def draw(self, scrollable_screen=None):
        if scrollable_screen is None:
            scrollable_screen = self.main_screen

        page_rect = self.rect.move(
                0,
                -self.parent_container.scroll_y
            )

        shadow = page_rect.move(
            8,
            8
        )

        pygame.draw.rect(
            scrollable_screen,
            (150, 150, 150),
            shadow
        )

        pygame.draw.rect(
            scrollable_screen,
            (255, 255, 255),
            page_rect
        )

        pygame.draw.rect(
            scrollable_screen,
            (170, 170, 170),
            page_rect,
            1
        )

        if self.show_page_number:
            label = self.font.render(
                f"Page {self.number}",
                True,
                (90, 90, 90)
            )

            scrollable_screen.blit(
                label,
                (
                    page_rect.centerx
                    - label.get_width() // 2,
                    page_rect.bottom - 40
                )
            )

        # Draw items on page
        for child_item in self.children:
            child_item.draw(scrollable_screen)