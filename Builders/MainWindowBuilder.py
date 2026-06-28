
import pygame
from Builders.ContainerBuilder import ContainerBuilder
from Builders.MenuBuilder import MenuBuilder
from Builders.ToolbarsBuilder import ToolbarBuilder
from DataClasses.Config.EventsConfig import TextInputBlinkTimer
from DataClasses.DialogConfigData import CommonDialogsConfig, ConfirmDialogsConfig
from DataClasses.MainWindowData import MainWindowConfig, MainWindowDimensions
from DataClasses.MainWindowData import MainWindowText
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Helpers.FileHelper import FileHelper
from Helpers.ScreeHelper import ScreenHelper
from Model.Dialogs.ConfirmDialog import ConfirmDialog
from Model.Timer import Timer
from Model.ApplicationState import ApplicationState
from Model.Dialogs.BasicDialog import BasicDialog
from Model.Menu.MenuBar import MenuBar
from Model.Containers.ScrollableContainer import ScrollableContainer
from Model.Containers.Window import Window

class MainWindowBuilder: 
    
    def __init__(self):
        self.event_handler = None
        self.main_window:Window = None
        self.main_box:ScrollableContainer = None
        self.menu_bar:MenuBar = None
        self.toolbar_grid = None
        self.window_canvass:pygame.Surface = None # main screen  
        self.app_state = None # singleton needed
        
    def build(self):
         self.init_window()\
            .build_toolbars()\
            .build_containers()\
            .build_menus() \
            .build_common_dialog()\
            .build_confirm_dialog()\
            .build_timers()\
         .init_app_state()
         return self.main_window

    """This must be first function to be called when building window and components."""
    def init_window(self):    
        WIDTH, HEIGHT, x, y = ScreenHelper.get_dimensions_by_ratio(
        width_ratio=MainWindowDimensions.WIDTH_RATIO, 
        height_ratio=MainWindowDimensions.HEIGHT_RATIO)

        asset_path = FileHelper.get_asset_images_paths() 
        bg_image_path = asset_path / "blue_background.jpg"
        icon_path = asset_path / "icon.png"

        self.main_window = Window(pygame.Rect(x, y, WIDTH, HEIGHT), bg_image_path, icon_path, MainWindowText.TITLE)
        # This is needed early because some components need to subscribe to window events during their build process, and they need access to the event handler for that. We can get the event handler from the main window since it's created in the main window's constructor.
        self.event_handler = self.main_window.get_event_handler()
        self.window_canvass = self.main_window.get_canvass()
        # register window for resize and quit events
        self.event_handler.subscribe(pygame.VIDEORESIZE, self.main_window)
        self.event_handler.subscribe(pygame.QUIT, self.main_window)        
        
        return self
   
    """This builds all toolbars and assigns them to main_window."""
    def build_toolbars(self):
        self.toolbar_grid = ToolbarBuilder(self.main_window, self.event_handler).build()
        self.main_window.add_child(self.toolbar_grid)        
        return self

    """Builds all containers that are direct children of main_window."""
    def build_containers(self):
        self.main_box = ContainerBuilder(self.main_window, self.event_handler).build()
        self.main_window.add_child(self.main_box)
        return self

    """Builds the main menu.Should be called last when rendering because of z-index"""
    def build_menus(self):
        self.menu_bar = MenuBuilder(self.main_window, self.event_handler).build()
        self.main_window.add_child(self.menu_bar)
        return self

    def build_common_dialog(self):        
        title_font = pygame.font.SysFont(CommonDialogsConfig.DIALOG_TITLE_FONT[0], 
                                        CommonDialogsConfig.DIALOG_TITLE_FONT[1])
        text_font = pygame.font.SysFont(CommonDialogsConfig.DIALOG_MESSAGE_FONT[0], 
                                        CommonDialogsConfig.DIALOG_MESSAGE_FONT[1])
        dialog_surface = pygame.Surface((400, 240))
        dialog_rect = dialog_surface.get_rect()
        dialog_rect.center = self.main_window.rect.center
        common_dialog = BasicDialog(CommonDialogsConfig.DIALOG_NAME, dialog_surface,
                                    dialog_rect, self.main_window.get_canvass(), title_font,text_font)
        self.main_window.set_common_dialog(common_dialog)
        self.main_window.add_child(common_dialog)
        return self
    
    def build_confirm_dialog(self):
        title_font = pygame.font.SysFont(ConfirmDialogsConfig.DIALOG_TITLE_FONT[0], 
                                        ConfirmDialogsConfig.DIALOG_TITLE_FONT[1])
        text_font = pygame.font.SysFont(ConfirmDialogsConfig.DIALOG_MESSAGE_FONT[0], 
                                        ConfirmDialogsConfig.DIALOG_MESSAGE_FONT[1])
        window_size = self.main_window.get_size()
        dialog_width = int((ConfirmDialogsConfig.DIALOG_SIZE_PERCENT[0] * window_size.width) / 100)
        dialog_height = int((ConfirmDialogsConfig.DIALOG_SIZE_PERCENT[1] * window_size.height) / 100)

        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_rect = dialog_surface.get_rect()
        dialog_rect.center = self.main_window.rect.center

        confirm_dialog = ConfirmDialog(ConfirmDialogsConfig, dialog_surface,
                                       dialog_rect, self.main_window.get_canvass(), title_font, text_font, 
                                       self.main_window)
        
        self.main_window.set_confirm_dialog(confirm_dialog)
        self.main_window.add_child(confirm_dialog)
        return self

    def build_timers(self):
        text_input_blink_timer = Timer(TextInputBlinkTimer.NAME, TextInputBlinkTimer.INTERVAL)
        self.event_handler.add_timer(text_input_blink_timer)
        return self
        
    def add_supported_events(self):
        self.main_window.set_supported_events( [pygame.VIDEORESIZE, pygame.QUIT])

    def get_main_window(self):
        return self.main_window
    
    def init_app_state(self):
        self.main_window.propagate_state()
        return self
    
    