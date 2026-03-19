
import pygame
from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from DataClasses.ToolbarData import ToolbarDimensions
from Model.Button import Button
from Model.Container import Container
from Model.DragAndDrop.DraggableNote import DraggableNoteButton
from Model.Geometry.Position import TextPosition
from Model.StaggeredLabelButton import StaggeredLabelButton


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
        self.button_type = ControlType.BUTTON
        
    def resize(self, new_width_ratio, new_height_ratio):
        super().resize(new_width_ratio, new_height_ratio) 

    def reposition_children(self, new_width_ratio=1, new_height_ratio=1):
        # resize the button margin for later use.
        self.button_margin = int(self.button_margin * new_width_ratio)    
        x = int(self.rect.x) + self.button_margin # add first margin
        for i, button in enumerate(self.children):  
            x = int(self.rect.x) + self.button_margin +\
                int(i * (button.rect.width + self.button_margin))
            button.rect.x = x
            button.rect.y = int(button.rect.y * new_height_ratio) 
        
        self.recalculate_size()

    def recalculate_size(self):
        total_width = self.button_margin  # start with left margin
        for button in self.children:
            total_width += button.rect.width + self.button_margin  # add button width and margin
        self.rect.width = total_width
        self.size = (self.rect.width, self.rect.height)

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

    def draw(self):
        super().draw()
        for button in self.children:
            button.draw()
        
   
   