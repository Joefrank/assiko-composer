
import pygame

from Model.Control import Control


class Container(Control):

    def __init__(self, 
                 rect, 
                 screen,
                 control_type,
                 control_name,
                 parent=None,
                 bg_color=(250, 250, 250), 
                 text_color=(0, 0, 0),
                 highlight_color=(200, 200, 255),
                 container_color=(220, 220, 220)):
        super().__init__(rect, control_type, control_name, parent) 
        self.bg_color = bg_color
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.container_color = container_color
        self.screen = screen   
   
    # -----------------------
    # Draw
    # border_tickness: 0 for filled, >0 for border only
    # -----------------------
    def draw(self,  highlight=False, border_tickness=0):
        color = self.highlight_color if highlight else self.container_color
        pygame.draw.rect(self.screen, color, self.rect, border_tickness)

    def add(self, item):
        self.items.append(item)
        item.container = self

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)

   