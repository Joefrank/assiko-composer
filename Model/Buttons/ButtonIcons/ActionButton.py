

import pygame

from DataClasses.ButtonConfigData import ActionButtonConfig
from DataClasses.ControlData import ControlType
from Model.Control import Control
from Model.Geometry.Size import Size


class ActionButton(Control):

    def __init__(self, rect, button_config: ActionButtonConfig, target_control):
        super().__init__(rect, ControlType.ACTION_BUTTON, button_config.name, target_control)
        self.tooltip = button_config.tooltip
        self.action = button_config.action
        self.icon_path = button_config.icon_path   
        self.size: Size = button_config.size  
               

    def move_y(self, offset_y):
        self.rect.y += offset_y

    def on_mouse_motion(self, event):     
         
        if self.rect.collidepoint(event.pos):
            print(f"mouse over") 
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            return True
        else:  
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            return False 
        
    def on_left_mouse_down(self, event):
        if self.rect.collidepoint(event.pos):
            print(f"click event: {event.pos}")