import pygame

from DataClasses.ControlData import ControlType
from Model.Control import Control


class DialogButton(Control):
    
    def __init__(self, rect, text, font, name, parent_dialog,
                 background_color=(100,100,100), 
                 text_color=(255, 255, 255)):
        super().__init__(rect, ControlType.DIALOG_BUTTON, name) 
        self.rect = pygame.Rect(rect)
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.font = font
        self.surface = parent_dialog.surface
        self.parent = parent_dialog
        self.hover = False
        self.action = None

    def draw(self):
        color = tuple(min(c + 25, 255) for c in self.background_color) \
            if self.hover else self.background_color

        #print(f"Drawing {self.text} at {self.rect}")
        
        pygame.draw.rect(
            self.surface,
            color,
            self.rect,
            border_radius=10
        )

        pygame.draw.rect(
            self.surface,
            self.text_color,
            self.rect,
            2,
            border_radius=10
        )

        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        self.surface.blit(text, text_rect)

    def set_action(self, action):
        self.action = action

    def on_mouse_motion(self, event):  
        actual_position = self.map_coordinates_to_parent(event.pos)

        if self.rect.collidepoint(actual_position):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            self.hover = True
            return True
        else:  
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            self.hover = False

        return self.hover 
        
    def on_left_mouse_down(self, event):
        actual_position = self.map_coordinates_to_parent(event.pos)

        if self.rect.collidepoint(actual_position):
            if self.action:
                print(f"Executing action target: {self.parent.target.name}")
                self.action(self.parent.target)
            return True

        return False

    def map_coordinates_to_parent(self, position):
        if self.parent:
            parent_position = (position[0] - self.parent.rect.x, position[1] - self.parent.rect.y)
            return parent_position
        return position
