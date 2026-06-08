
import pygame


class DraggableItem:

    

    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.FONT = pygame.font.SysFont("segoeui", 20, bold=True)

    def draw(self, surface, scroll_x, scroll_y):

        draw_rect = self.rect.move(
            -scroll_x,
            -scroll_y
        )

        pygame.draw.rect(
            surface,
            self.color,
            draw_rect,
            border_radius=8
        )

        pygame.draw.rect(
            surface,
            (40, 40, 40),
            draw_rect,
            2,
            border_radius=8
        )

        text_surface = self.FONT.render(
            self.text,
            True,
            (0, 0, 0)
        )

        surface.blit(
            text_surface,
            (
                draw_rect.x + 10,
                draw_rect.y + 10
            )
        )
