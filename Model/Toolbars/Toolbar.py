
import pygame
from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from DataClasses.ToolbarData import ToolbarDimensions
from Model.Button import Button
from Model.Container import Container
from Model.DragAndDrop.DraggableNote import DraggableNoteButton
from Model.Position import TextPosition


class Toolbar(Container):    
    
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
        super().__init__(rect, screen, ControlType.TOOLBAR, name, None, bg_color, text_color, 
                         highlight_color, container_color)       
        self.button_width = button_width
        self.button_height = button_height
        self.button_margin = button_margin
        self.button_text_center = button_text_center
        self.buttons_draggable = buttons_draggable
        self.grid_coordinates = grid_coordinates  # (column, row) tuple
        self.grid_spacing = grid_spacing
        self.set_z_index(ControlZIndex.LEVEL2) 
        self.is_resizable = True

    def create_buttons(self, icons:list[tuple[str, str]], font, toolbar_height, # pass height of toolbar here
                    text_color, bg_color, hover_text_color, hover_bg_color, border_radius=0):
        button_top_padding = (toolbar_height - self.button_height) // 2
        x= ToolbarDimensions.BUTTON_MARGIN    
        for icon, action in icons:
            button_rect = pygame.Rect(x, button_top_padding, self.button_width, self.button_height)
            button = Button(action, button_rect, icon, action, font, border_radius, 
                            text_color, bg_color, hover_text_color, hover_bg_color, self.buttons_draggable)
            button.set_parent(self, offset_x=x, offset_y=button_top_padding)
            if self.buttons_draggable:
                button.add_supported_events([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
            else:
                button.add_supported_events([pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION])

            self.add_button(button)
            x += self.button_width + self.button_margin
        return self.children

    def resize(self, new_width_ratio, new_height_ratio):
        print(f"Before resize: Toolbar rect: {self.rect}")
        super().resize(new_width_ratio, new_height_ratio)
        # Reposition buttons based on new size
        # x = int(self.rect.x * new_width_ratio) + int(self.button_margin * new_width_ratio)
        # for button in self.children:
        #     button.rect.x = x
        #     button.rect.y = int(button.rect.y * new_height_ratio) 
        #     x += button.rect.width + (self.button_margin * new_width_ratio)
        # self.rect.x = int(self.rect.x * new_width_ratio)
        # self.rect.y = int(self.rect.y * new_height_ratio)
        # self.rect.width = int(self.rect.width * new_width_ratio)
        # self.rect.height = int(self.rect.height * new_height_ratio)
        print(f"After resize: Toolbar rect: {self.rect}")


    def add_button(self, button):      
        self.children.append(button)
        button.container = self
        self.rect.width += button.rect.width + self.button_margin 

    def add_draggable_items(self, items: list[DraggableNoteButton]):
        x = self.rect.left + self.button_margin
        for item in items:
            item.rect.x = x
            item.rect.y = self.rect.top + 10
            self.add_button(item)
            x += item.rect.width + self.button_margin    

    def draw(self, highlight=False):
        super().draw(highlight)
        for button in self.children:
            button.draw(self.screen, self.button_text_center)
   
   