import pygame

from DataClasses.ControlData import ControlType
from Model.Control import Control


class DialogButton(Control):
    
    def __init__(self, rect, text, font, surface, name, 
                 background_color=(100,100,100), 
                 text_color=(255, 255, 255)):
        super().__init__(rect, ControlType.DIALOG_BUTTON, name) 
        self.rect = pygame.Rect(rect)
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.font = font
        self.surface = surface
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
        print(f"Mouse motion event at {event.pos} for button {self.name}")    
        if self.rect.collidepoint(event.pos):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            self.hover = True
            return True
        else:  
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            self.hover = False

        return self.hover 
        
    def on_left_mouse_down(self, event):
        if self.rect.collidepoint(event.pos):
            # check this is set self.action and call it.
            print("left mouse called on dialog button")
