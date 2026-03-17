import pygame

from DataClasses.ButtonData import ButtonConfig
from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Helpers.ScreeHelper import ScreenHelper
from Model.Toolbars.ToolbarActivator import ToolbarActivator
from Model.Control import Control
from Model.Position import TextPosition

class Button(Control):
    
   
    def __init__(self, screen, name, rect, text, action, font, font_details, border_radius=0, text_position=TextPosition.CENTER,
                 text_color=ButtonConfig.TEXT_DEFAULT_COLOR, bg_color=ButtonConfig.BTN_DEFAULT_COLOR, hover_text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
                 hover_bg_color=ButtonConfig.BTN_DEFAULT_HOVER, is_draggable=False):
        super().__init__(rect, ControlType.TOOLBARITEM, name)   
        self.screen = screen
        self.is_draggable = is_draggable
        self.text = text
        self.action = action
        self.font = font
        self.font_details = font_details
        self.border_radius = border_radius
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_text_color = hover_text_color
        self.hover_bg_color = hover_bg_color
        self.container = None
        self.activator = ToolbarActivator()
        self.dragging = False
        self.offset = (0, 0)
        self.dragged_symbols = []
        self.current_dragged_symbol = None
        self.set_z_index(ControlZIndex.LEVEL3)
        self.is_resizable = True 
        self.text_position = text_position       
       

    def draw(self):
        text_color = self.draw_button_frame()  # get the appropriate text color based on hover state
        self.draw_label(text_color)  # pass text position to draw_label method       
        if self.is_draggable:
            # Draw the dragging copy if one exists
            self.draw_dragged_icons()
       
    def draw_button_frame(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_bg_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        text_color = self.hover_text_color if self.rect.collidepoint(mouse_pos) else self.text_color
        pygame.draw.rect(self.screen, color, self.rect, border_radius=self.border_radius)
        return text_color

    def draw_label(self, text_color):
        label = self.font.render(self.text, True, text_color)
        label_rect = label.get_rect()
        gap = 8  # pixels between rect and label

        if self.text_position == TextPosition.CENTER:
            label_rect.center = self.rect.center
        elif self.text_position == TextPosition.TOP_CENTER:
            label_rect.centerx = self.rect.centerx
            label_rect.centery = self.rect.centery - gap
        elif self.text_position == TextPosition.BOTTOM_CENTER:
            label_rect.centerx = self.rect.centerx
            label_rect.centery = self.rect.centery + gap

        self.screen.blit(label, label_rect)
    
    def draw_dragged_icons(self):
         for dragged_note in self.dragged_symbols:
                label_copy = self.font.render(self.text, True, (0, 0, 0))
                copy_rect = label_copy.get_rect(center=dragged_note.center)
                self.screen.blit(label_copy, copy_rect)    

    """ put order in subscribers so that if item in top of line responds first then it won't pass to item below it."""
    def on_left_mouse_down(self, event):
        if self.rect.collidepoint(event.pos):
            if self.is_draggable:
                self.dragging = True
                # Create a rect for the dragging copy
                self.current_dragged_symbol = self.rect.copy()
                self.dragged_symbols.append(self.current_dragged_symbol)
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
            self.dragged_symbols.remove(self.current_dragged_symbol)
            self.current_dragged_symbol = None

    def on_mouse_motion(self, event):  
        if self.is_draggable and self.dragging:
            self.current_dragged_symbol.x = event.pos[0] + self.offset[0]
            self.current_dragged_symbol.y = event.pos[1] + self.offset[1]     
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

    def resize(self, new_width_ratio, new_height_ratio):
         # change size of this font
        self.font_details = (self.font_details[0], int(self.font_details[1] * new_height_ratio))
        self.font = ScreenHelper.create_font(self.font_details)        
        return super().resize(new_width_ratio, new_height_ratio)