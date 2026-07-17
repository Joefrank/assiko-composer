import sys
import pygame
from Builders.TextItemBuilder import TextItemBuilder
from Builders.DynamicStaffBuilder import DynamicStaffBuilder
from DataClasses.Config.ScreenConfig import SupportedLanguages
from DataClasses.ControlData import ControlType
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Helpers.FileHelper import FileHelper
from Helpers.Translator import Translator
from Model.ApplicationState import ApplicationState
from Model.Control import Control
from Model.Dialogs.BasicDialog import BasicDialog
from Model.Geometry.Size import Size


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
        self.event_handler = MainWindowEventHandler()
        self.app_state = ApplicationState(self)        
        self.__dialogs_cache = {}
        self.dialog_builder = None
        language_path = FileHelper.get_path("Assets\\Languages")
        self.__translator = Translator(root = language_path, default_language=SupportedLanguages.FRENCH)
        self.app_state.set_translator(self.__translator)
        self.score_document = None
        self.__dynamic_staff_builder = DynamicStaffBuilder(self)
        self.__text_item_builder = TextItemBuilder(self)
       
    @property
    def common_dialog(self):        
        return next(
            (child for child in self.children if isinstance(child, BasicDialog)),
                None
            )
    
    @property
    def translator(self):
        return self.__translator
    
    @property
    def staff_builder(self):
        return self.__dynamic_staff_builder
    
    @property
    def text_item_builder(self):
        return self.__text_item_builder
    
    def set_score_document(self, score_document):
        self.score_document = score_document

    def get_score_document(self):
        return self.score_document

    def get_dialog(self, dialog_id):
        return self.__dialogs_cache.get(dialog_id)
    
    def add_dialog(self, dialog_id, dialog):
        self.__dialogs_cache[dialog_id] = dialog

    def get_state(self):
        return self.app_state    

    def get_canvass(self):
        return self.screen   
   
    def set_dialog_builder(self, dialog_builder):
        self.dialog_builder = dialog_builder

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

    # def show_common_dialog(self, content, title:str ="", size:Size=None):
    #     self.common_dialog.set_content(title, main_content=content) 
    #     if not size is None:
    #         self.common_dialog.set_size(size.width, size.height)
    #     self.common_dialog.show()

    # def show_confirm_dialog(self, content, title:str ="", size:Size=None):
    #     self.confirm_dialog.set_content(title, main_content=content) 
    #     if not size is None:
    #         self.confirm_dialog.set_size(size.width, size.height)
    #     self.confirm_dialog.show()

    def propagate_state(self):
        for child in self.children:
            child.set_app_state(self.app_state)

    def get_event_handler(self):
        return self.event_handler
    
    def handle_events(self, dt:int):
        self.event_handler.handle_events(dt)
        self.re_draw_component()