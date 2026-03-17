
# --------------------------------------------------
# Menu Bar
# --------------------------------------------------
import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Control import Control


class MenuBar(Control):
    def __init__(self, width:int, menu_height:int, menu_item_spacing:int, menu_bg_color:tuple, screen:pygame.Surface):
        super().__init__(rect=pygame.Rect(0,0,width,menu_height), control_type=ControlType.MENUBAR ,name="Main Menue") 
        #self.menus = []
        self.menu_height = menu_height
        self.menu_bg_color = menu_bg_color
        self.next_x_offset = self.menu_item_spacing = menu_item_spacing
        self.width = width
        self.width_percent_of_window = 100
        self.height_percent_of_window = 7  
        self.left_margin = 0
        self.top_margin = 0  
        self.set_z_index(ControlZIndex.LEVEL3) 
        self.is_resizable = True
        self.screen = screen

    def add_menu(self, menu):
        self.next_x_offset += sum(m.rect.width for m in self.children) + self.menu_item_spacing * len(self.children)       
        menu.set_position(self.next_x_offset)
        self.children.append(menu)
       
    def resize(self, new_width_ratio, new_height_ratio):
        if not self.is_resizable:
            return
        _, children_sizes = super().resize(new_width_ratio, new_height_ratio)

        # re-adjust x position of each child and calculate of all childrent.
        self.next_x_offset = self.menu_item_spacing * new_width_ratio
      
        for i, child in enumerate(self.children):
            child.set_position(self.next_x_offset)
            self.next_x_offset += child.rect.width + (self.menu_item_spacing * new_width_ratio)
        return self.size, children_sizes

    def draw(self):       
        pygame.draw.rect(self.screen, self.menu_bg_color, self.rect)
        any_open = any(m.open for m in self.children)
        for m in self.children:
            m.draw(self.screen, hover_open=any_open)

    # def resize(self, new_width, new_height, left_margin=0, top_margin=0):
    #     self.width = new_width * self.width_percent_of_window / 100
    #     self.menu_height = new_height * self.height_percent_of_window / 100
    #     self.left_margin = left_margin
    #     self.top_margin = top_margin
    #     self.draw(self.screen)

    def get_dimensions(self):
        return self.rect.width, self.rect.height
