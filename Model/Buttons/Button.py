import pygame

from DataClasses.ButtonConfigData import ButtonConfig
from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Helpers.ScreeHelper import ScreenHelper
from Model.Toolbars.ToolbarActivator import ToolbarActivator
from Model.Control import Control
from Model.Geometry.Position import TextPosition

class Button(Control):
    
    def __init__(self, config: ButtonConfig):
        rect = pygame.Rect(config.position[0], config.position[1], config.toolbar.button_width, config.toolbar.button_height)
        super().__init__(rect, ControlType.TOOLBARITEM, config.action)  
       
    # def __init__(self, screen, name, rect, text, tooltip, font, font_details, border_radius=0, text_position=TextPosition.CENTER,
    #              text_color=ButtonConfig.TEXT_DEFAULT_COLOR, bg_color=ButtonConfig.BTN_DEFAULT_COLOR, hover_text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
    #              hover_bg_color=ButtonConfig.BTN_DEFAULT_HOVER, is_draggable=False, action=None):
    #     super().__init__(rect, ControlType.TOOLBARITEM, name)   
        self.screen = config.screen
        self.is_draggable = config.draggable_icons
        self.text = config.icon
        self.tooltip = config.action
        self.action = config.action if config.action_value is None else config.action_value
        self.font = config.font
        self.font_details = config.font_details
        self.border_radius = config.border_radius
        self.text_color = config.text_color
        self.bg_color = config.bg_color
        self.hover_text_color = config.hover_text_color
        self.hover_bg_color = config.hover_bg_color
        self.container = None
        self.activator = ToolbarActivator()
        self.dragging = False
        self.offset = (0, 0)
        self.dragged_symbols = []
        self.current_dragged_symbol = None
        self.set_z_index(ControlZIndex.LEVEL3)
        self.is_resizable = True 
        self.text_position = config.toolbar.button_text_center       
       

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
            else:# Mouse click
                method = getattr(self.activator, self.action)
                method()
            return True  # Event handled
        return False  # Event not handled

    def on_left_mouse_up(self, event):
        # Notify state of symbol drop if it's draggable.
        print(f"button mouse up")
        if self.current_dragged_symbol and self.app_state:
            self.app_state.save_dropped_symbol(self.current_dragged_symbol, 
                                               self.action, self.parent.drop_action)        
            self.dragged_symbols.remove(self.current_dragged_symbol)
            self.current_dragged_symbol = None
            
        self.dragging = False
        
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
        self.parent = parent
        self.rect.x = parent.rect.left + offset_x
        self.rect.y = parent.rect.top + offset_y

    def resize(self, new_width_ratio, new_height_ratio):
         # change size of this font
        self.font_details = (self.font_details[0], int(self.font_details[1] * new_height_ratio))
        self.font = ScreenHelper.create_font(self.font_details)        
        return super().resize(new_width_ratio, new_height_ratio)
    
    def reposition_children(self, new_width_ratio, new_height_ratio):
        pass