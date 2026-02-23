import pygame
import sys

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Toolbars.ToolbarActivator import ToolbarActivator
from Model.Control import Control
from Model.Position import TextPosition

class Button(Control):
    BTN_COLOR = (70, 70, 70)
    BTN_HOVER = (100, 100, 100)
    TEXT_COLOR = (255, 255, 255)    
   
    def __init__(self, name, rect, text, action, font, border_radius=0,
                 text_color=TEXT_COLOR, bg_color=BTN_COLOR, hover_text_color=TEXT_COLOR, 
                 hover_bg_color=BTN_HOVER, is_draggable=False):
        super().__init__(rect, ControlType.TOOLBARITEM, name)   
        self.is_draggable = is_draggable
        self.text = text
        self.action = action
        self.font = font
        self.border_radius = border_radius
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_text_color = hover_text_color
        self.hover_bg_color = hover_bg_color
        self.container = None
        self.activator = ToolbarActivator()
        self.dragging = False
        self.offset = (0, 0)
        self.dragged_notes = []
        self.current_dragged_note = None
        self.set_z_index(ControlZIndex.LEVEL1)
        self.is_resizable = True 
       

    def draw(self, surface, text_center_position):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_bg_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        text_color = self.hover_text_color if self.rect.collidepoint(mouse_pos) else self.text_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)        
        
        label = self.font.render(self.text, True, text_color)
        label_rect = label.get_rect()
        gap = 8  # pixels between rect and label

        if text_center_position == TextPosition.CENTER:
            label_rect.center = self.rect.center
        elif text_center_position == TextPosition.TOP_CENTER:
            label_rect.centerx = self.rect.centerx
            label_rect.centery = self.rect.centery - gap
        elif text_center_position == TextPosition.BOTTOM_CENTER:
            label_rect.centerx = self.rect.centerx
            label_rect.centery = self.rect.centery + gap

        surface.blit(label, label_rect)

        if self.is_draggable:
             # Draw the dragging copy if one exists
            for dragged_note in self.dragged_notes:
                label_copy = self.font.render(self.text, True, (0, 0, 0))
                copy_rect = label_copy.get_rect(center=dragged_note.center)
                surface.blit(label_copy, copy_rect)
       
    """ put order in subscribers so that if item in top of line responds first then it won't pass to item below it."""
    def on_left_mouse_down(self, event):
        if self.rect.collidepoint(event.pos):
            if self.is_draggable:
                self.dragging = True
                # Create a rect for the dragging copy
                self.current_dragged_note = self.rect.copy()
                self.dragged_notes.append(self.current_dragged_note)
                # offset keeps the cursor from snapping to top-left
                self.offset = (
                    self.rect.x - event.pos[0],
                    self.rect.y - event.pos[1]
                )
            else:
                method = getattr(self.activator, self.action)
                method()
            return True  # Event handled
        return False  # Event not handled

    def on_left_mouse_up(self, event):       
        self.dragging = False
        if self.rect.collidepoint(event.pos):# we don't want to leave the item dragged on the button.
            self.dragged_notes.remove(self.current_dragged_note)
            self.current_dragged_note = None

    def on_mouse_motion(self, event):  
        if self.is_draggable and self.dragging:
            self.current_dragged_note.x = event.pos[0] + self.offset[0]
            self.current_dragged_note.y = event.pos[1] + self.offset[1]     
        return self.handle_hover(event.pos)

    def handle_hover(self, mouse_pos):       
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            return True
        else:  
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            return False   

    def set_parent(self, parent, offset_x=0, offset_y=0):
        self.container = parent
        self.rect.x = parent.rect.left + offset_x
        self.rect.y = parent.rect.top + offset_y