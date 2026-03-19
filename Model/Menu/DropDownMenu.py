# --------------------------------------------------
# Dropdown Menu
# --------------------------------------------------
import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from DataClasses.MenuData import MenuDimensions
from Model.Control import Control
from Model.Menu.MenuActivator import MenuActivator
from Model.Geometry.Position import Position


class DropdownMenu(Control):
    def __init__(self, activator, label:str, width:int, menu_bar_height:int, item_height:int,
                 menu_hover_color:tuple, menu_bg_color:tuple, big_font:pygame.font.Font, small_font:pygame.font.Font,
                 drop_bg_color:tuple=(55, 55, 55), drop_hover_color:tuple=(95, 95, 95), border_color:tuple=(110, 110, 110),
                 shadow:tuple=(0, 0, 0, 90), radius:int=8, text_color:tuple=(235, 235, 235)):
        super().__init__(pygame.Rect(0, 0, width, menu_bar_height * MenuDimensions.MENU_HEIGHT_RATIO), ControlType.MENU, label)
        self.label = label
        self.items = []
        self.item_rects = []
        self.open = False
        self.menu_bar_height = menu_bar_height
      
        self.menu_hover_color = menu_hover_color
        self.menu_bg_color = menu_bg_color
        self.radius = radius
        self.text_color = text_color
        self.big_font = big_font
        self.small_font = small_font        
        self.item_height = item_height
        self.drop_bg_color = drop_bg_color
        self.drop_hover_color = drop_hover_color
        self.border_color = border_color
        self.shadow = shadow        
       
        self.activator = activator
        self.set_z_index(ControlZIndex.LEVEL2) 
        self.is_resizable = True

    def set_position(self, x_offset:int):        
        self.rect = pygame.Rect(x_offset, self.rect.height * 0.2, self.rect.width, self.rect.height)
        for i, item in enumerate(self.items):
            item.set_position(Position(x_offset, self.rect.y + self.rect.height + (i * item.rect.height)))

    # Handle events for menu and shortcuts
    def on_left_mouse_down(self, event):        
        if self.rect.collidepoint(event.pos):
            self.open = not self.open            
            return True  # Event handled
        else:
            self.open = False
            return False

    def on_item_clicked(self):
        #self.open = False
        pass    


    def draw(self, surface, hover_open=False):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)

        if hover_open and hover:
            self.open = True

        pygame.draw.rect(
            surface,           
            (self.menu_hover_color if hover else self.menu_bg_color),
            self.rect,
            border_radius=self.radius,
        )

        label = self.big_font.render(self.label, True, self.text_color)
        surface.blit(label, label.get_rect(center=self.rect.center))

        self.item_rects = []
        #
        if self.open:
            
            self.draw_items(surface) 
        else:
            self.hide_items()                  

    def draw_items(self, surface):
        width = MenuDimensions.MENU_ITEM_WIDTH_RATIO * self.rect.width
        height = len(self.items) * self.item_height
        drop_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, width, height)

        self.draw_shadow(surface, drop_rect)
        pygame.draw.rect(surface, self.drop_bg_color, drop_rect, border_radius=self.radius)
        pygame.draw.rect(surface, self.border_color, drop_rect, 1, border_radius=self.radius)
        
        for item in self.items:
            item.visible = True
            item.draw(surface)

    def hide_items(self):
        for item in self.items:
            item.visible = False

    def add_item(self, item):
        item.set_parent(self)
        self.items.append(item)

    # Shadow Helper
    # --------------------------------------------------
    def draw_shadow(self,surface, rect):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill(self.shadow)
        surface.blit(s, (rect.x + 2, rect.y + 2))

