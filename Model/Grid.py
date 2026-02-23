

import pygame
from Model.Container import Container

"""This is a container that doesn't get displayed itself, we could display lines later though."""
class Grid(Container):
    def __init__(self, 
                 rect, 
                 grid_size,
                screen, 
                control_type, 
                control_name, 
                parent=None, show_grid_lines=False, grid_spacing=(0, 0)):
        super().__init__(rect, screen, control_type, control_name, parent) 
        self.grid_size = grid_size  # (rows, cols), the actual size will depend on the number of controls added to the grid and their sizes
        self.grid_spacing = grid_spacing  # (horizontal_spacing, vertical_spacing)
        self.padding = (0, 0)  # (horizontal_padding, vertical_padding)
        self.show_grid_lines = show_grid_lines  # for debugging layout, we can toggle this on to see the grid lines

    def draw(self, highlight=False, border_tickness=0):
        if self.show_grid_lines:
            # draw grid lines for debugging layout
            for row in range(self.grid_size[0] + 1):
                y = self.rect.y + row * (self.rect.height // self.grid_size[0]) + self.padding[1]
                pygame.draw.line(self.screen, (200, 200, 200), (self.rect.x, y), (self.rect.x + self.rect.width, y))
            for col in range(self.grid_size[1] + 1):
                x = self.rect.x + col * (self.rect.width // self.grid_size[1]) + self.padding[0]
                pygame.draw.line(self.screen, (200, 200, 200), (x, self.rect.y), (x, self.rect.y + self.rect.height))
        