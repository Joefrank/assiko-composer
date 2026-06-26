

import pygame

from DataClasses.ButtonConfigData import ActionButtonConfig
from DataClasses.ControlData import ControlType
from Model.Geometry.Size import Size
from Model.Score.ScoreControl import ScoreControl


class ActionButton(ScoreControl):

    def __init__(self, rect, button_config: ActionButtonConfig, target_control):
        super().__init__(rect, ControlType.ACTION_BUTTON, button_config.name, target_control)
        self.tooltip = button_config.tooltip
        self.action = button_config.action
        self.icon_path = button_config.icon_path   
        self.size: Size = button_config.size  
               

    def move_y(self, offset_y):
        self.rect.y += offset_y

    def on_mouse_motion(self, event):    
        # This call cascades to parent viewport to map coordinates
        real_coordinates = self.parent.map_coordinates_in_viewport(event.pos)  

        if self.rect.collidepoint(real_coordinates):         
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            return True
        else:  
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            return False 
        
    def on_left_mouse_down(self, event):
        real_coordinates = self.parent.map_coordinates_in_viewport(event.pos)    

        if self.rect.collidepoint(real_coordinates):          
            function = getattr(self.parent, self.action, None)
            if function:
                function(self)