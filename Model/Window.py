import sys
import pygame
from DataClasses.ControlData import ControlType
from Model.Control import Control
from Model.Size import Size


class Window(Control):
    def __init__(self, 
                rect:pygame.Rect,
                bg_image_path:str, 
                icon_path:str, 
                title="Application Window"):
        super().__init__(rect, control_type=ControlType.WINDOW , name="Main Window")   
        self.width = rect.width
        self.height = rect.height
        self.title = title
        self.is_open = False
        self.bg_image_path = bg_image_path
        self.icon_path = icon_path
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)        

    def get_canvass(self):
        return self.screen   
   
    def draw(self) -> pygame.Surface:       
        pygame.display.set_caption(self.title)
        self.draw_icon()   
        self.draw_children_controls()

    def re_draw_component(self):
        self.draw_tiled_background(self.screen)  
        self.draw_children_controls()  
        
    def draw_children_controls(self):
        # draw children controls in order of their z-index (lower z-index first)
        ordered_children = sorted(self.children, key=lambda c: c.z_index)
        for child in ordered_children:
            if child.visible:
                child.draw()      
  
    # --------------------------------------------------
    # Load Background Tile
    # --------------------------------------------------
    def draw_tiled_background(self,screen:pygame.Surface):
        background_tile = pygame.image.load(self.bg_image_path).convert()
        tile_w = background_tile.get_width()
        tile_h = background_tile.get_height()      

        for x in range(0, self.width, tile_w):
            for y in range(0, self.height, tile_h):
                screen.blit(background_tile, (x, y))

    def draw_icon(self):
        icon = pygame.image.load(self.icon_path).convert()
        pygame.display.set_icon(icon)
        
    # def resize_children(self):
    #     for child in self.children:
    #         if hasattr(child, 'resize'):
    #             child.resize(self.width, self.height)

    def add_child(self, control:Control):
        self.children.append(control)
  
    def get_size(self):
        return Size(self.width, self.height)
    
    def get_dimensions(self):
        return self.width, self.height
    
    # Event handlers for window-level events
    def on_video_resize(self, event):
        width_ratio = event.w / self.width
        height_ratio = event.h / self.height
        self.width = event.w
        self.height = event.h
        self.resize_children(width_ratio, height_ratio)

    def on_quit(self, event):        
        pygame.quit()
        sys.exit()
    