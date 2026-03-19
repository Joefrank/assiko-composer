

import pygame

from DataClasses.ButtonData import ButtonType
from DataClasses.ControlData import ControlType
from Model.Geometry.Position import TextPosition
from Model.Toolbars.Toolbar import Toolbar


class StaggeredButtonToolbar(Toolbar):

    def __init__(self, 
                 rect, 
                 screen:pygame.Surface, 
                 name,
                 button_width,
                 button_height,
                 button_margin,
                 bg_color=(250, 250, 250, 50), 
                 text_color=(0, 0, 0),
                 highlight_color=(200, 200, 255),
                 container_color=(220, 220, 220, 100),
                 button_text_center=TextPosition.CENTER,
                 buttons_draggable=False,
                 grid_coordinates=None,
                 grid_spacing=0):
        super().__init__(rect,screen, name, button_width, button_height, button_margin,
                 bg_color, text_color, highlight_color, container_color, button_text_center,
                 buttons_draggable, grid_coordinates, grid_spacing)
        self.button_type = ButtonType.STAGGERED_SYMBOL_BUTTON
        self.test_draw = True

    def draw(self):
        super().draw()

    def reset_children_positions(self):
        previous_button = None       
        for i, button in enumerate(self.children):            
            if previous_button == None:                  
                new_x = int(self.rect.x + self.button_margin) 
            else:
                new_x = int(previous_button.rect.x + previous_button.rect.width + self.button_margin) 
               
            x_difference = (new_x - button.rect.x)            
            button.rect.x = new_x # this adjust the x coordinate of button
            previous_button = button
            button.reset_children_positions(x_difference)           
        
        self.recalculate_size()

    def resize(self, new_width_ratio, new_height_ratio):
        super().resize_only(new_width_ratio, new_height_ratio)
        self.resize_children(new_width_ratio, new_height_ratio)
        self.reposition_children(new_width_ratio, new_height_ratio)
        
    def reposition_children(self, new_width_ratio=1, new_height_ratio=1):  
        self.button_margin *= new_width_ratio  
        self.button_height *= new_height_ratio   
        x_offset = self.rect.x + self.button_margin # add first margin
        button_top_padding = (self.rect.height - self.children[0].rect.height) // 2
        for button in self.children:
            h_move =  x_offset - button.rect.x
            v_move = (self.rect.y + button_top_padding) - button.rect.y
            button.rect.x = x_offset
            button.rect.y = self.rect.y + button_top_padding
            x_offset += button.rect.width + self.button_margin
            button.move_children(h_move, v_move)
        self.recalculate_size()