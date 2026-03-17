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
                 container_color=(220, 220, 220),
                 border_tickness=0):
        super().__init__(rect, control_type, control_name, parent) 
        self.bg_color = bg_color
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.container_color = container_color
        self.border_tickness = border_tickness
        self.screen = screen   
   
    # -----------------------
    # Draw
    # border_tickness: 0 for filled, >0 for border only
    # -----------------------
    def draw(self):        
        if self.border_tickness > 0:
            pygame.draw.rect(self.screen, self.bg_color, self.rect)
        pygame.draw.rect(self.screen, self.container_color, self.rect, self.border_tickness)
        for child in self.children:
            child.draw()

    def add(self, item):
        self.items.append(item)
        item.container = self

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)

