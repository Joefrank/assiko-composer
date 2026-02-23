

import pygame
from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Control import Control


class DropDownMenuItem(Control):
    def __init__(self, activator, text:str, action:str, rect:pygame.Rect,
                 text_color, bg_color, hover_text_color, hover_bg_color,
                 border_radius=0, font=None, key_shortcut=None):
        super().__init__(rect, ControlType.MENU, text)
        self.text = text
        self.action = action
        self.hover_color = hover_bg_color
        self.hover_text_color = hover_text_color
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.font = font
        self.key_shortcut = key_shortcut
        self.activator = activator
        self.visible = False  # Menu items are hidden by default
        self.set_z_index(ControlZIndex.LEVEL2) 
        self.is_resizable = True

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)       
        item_text = self.font.render(self.text, True, self.text_color if not self.hover_text_color else self.hover_text_color)
        screen.blit(item_text, (self.rect.x + 12, self.rect.y + 6)) 

    def set_position(self, position):
        self.rect.x = position.x
        self.rect.y = position.y

    def on_left_mouse_down(self, event):        
        if self.rect.collidepoint(event.pos):           
           self.execute() 
           return True  # Event handled
        return False  # Event not handled  

    def on_left_mouse_up(self, event):
        self.parent.on_item_clicked()  # Notify parent menu to close

    def on_key_down(self, event):
        if self.key_shortcut and event.key == self.key_shortcut:
           self.execute() 

    def execute(self):
        method = getattr(self.activator, self.action)
        method()   
           