

import pygame
from DataClasses.MainWindowData import ControlZIndex
from Model.Containers.Container import Container

"""This is a container that doesn't get displayed itself, we could display lines later though."""
class Grid(Container):
    def __init__(self, 
                 rect,
                 screen, 
                 control_type, 
                 control_name, 
                 parent=None, 
                 show_grid_lines=False, 
                 grid_spacing=(0, 0)):
        super().__init__(rect, screen, control_type, control_name, parent, border_tickness=1) 
        self.grid_sizes = None  # (rows, cols), the actual size will depend on the number of controls added to the grid and their sizes
        self.grid_spacing = grid_spacing  # (horizontal_spacing, vertical_spacing)
        self.padding = (0, 0)  # (horizontal_padding, vertical_padding)
        self.show_grid_lines = show_grid_lines  # for debugging layout, we can toggle this on to see the grid lines
        self.border_tickness = 1
        self.is_resizable = True
        self.set_z_index(ControlZIndex.LEVEL2)
    
    def set_grid_sizes(self, sizes):
        self.grid_sizes = sizes

    def draw(self):
        super().draw()
        if self.show_grid_lines:
            # draw grid lines for debugging layout
            no_rows = len(self.grid_sizes)
            for row in range(no_rows + 1):
                y = self.rect.y + row * (self.rect.height // no_rows) + self.padding[1]
                pygame.draw.line(self.screen, (200, 200, 200), (self.rect.x, y), (self.rect.x + self.rect.width, y))
            no_cols = max(self.grid_sizes)

            for col in range(no_cols + 1):
                x = self.rect.x + col * (self.rect.width // no_cols) + self.padding[0]
                pygame.draw.line(self.screen, (200, 200, 200), (x, self.rect.y), (x, self.rect.y + self.rect.height))
        
    def resize(self, new_width_ratio, new_height_ratio):
        self.grid_spacing = (int(self.grid_spacing[0] * new_width_ratio), int(self.grid_spacing[1] * new_height_ratio))
        super().resize_only(new_width_ratio, new_height_ratio)
        super().reset_position(new_width_ratio, new_height_ratio)
        self.resize_children(new_width_ratio, new_height_ratio)
        self.reposition_children(new_width_ratio, new_height_ratio)
    
    def reposition_children(self, new_width_ratio, new_height_ratio):

        for row_index in range(len(self.grid_sizes) + 1):
            # Get all children with matching row, ordered by column
            row_children = sorted([child for child in self.children if child.grid_coordinates[0] == row_index], key=lambda child: child.grid_coordinates[1])
            original_x = self.rect.x
            # Loop through found children and reposition them
            for child in row_children:
                child.rect.x = original_x
                child.rect.y = int(child.rect.y * new_height_ratio)
                child.reposition_children(new_width_ratio, new_height_ratio)  
                original_x += child.rect.width + self.grid_spacing[0]

        # for child in self.children:            
        #     child.rect.x = original_x
        #     child.rect.y = int(child.rect.y * new_height_ratio)
        #     child.reposition_children(new_width_ratio, new_height_ratio)  
        #     # first coordinate is row index and second is column index.
        #     if child.grid_coordinates[1] == self.grid_size[1] - 1:  # if it's not in the first column, we calculate x based on original_x, column index, child width and horizontal spacing
        #         original_x = self.rect.x  # reset original_x for first column, we are using a grid 2D array
        #     else:
        #         original_x += child.rect.width + self.grid_spacing[0] 
           
            
          