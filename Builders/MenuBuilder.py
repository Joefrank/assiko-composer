
import pygame
from DataClasses.MenuData import MenuColorConfig, MenuDimensions, MenuFontConfig , MenuItemsData
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Model.Menu.DropDownMenu import DropdownMenu
from Model.Menu.DropDownMenuItem import DropDownMenuItem
from Model.Menu.MenuActivator import MenuActivator
from Model.Menu.MenuBar import MenuBar
from Model.Size import Size


class MenuBuilder:
    def __init__(self, window_dimensions:Size, event_handler:MainWindowEventHandler):
        self.window_dimensions = window_dimensions
        self.event_handler = event_handler
        self.menu_bar = None
        self.MENU_BAR_HEIGHT = self.window_dimensions.height * MenuDimensions.MENU_BAR_HEIGHT_RATIO
        self.BIG_FONT = pygame.font.SysFont("segoeui", MenuFontConfig.BIG_FONT_SIZE, bold=True)
        self.SMALL_FONT = pygame.font.SysFont("segoeui", MenuFontConfig.SMALL_FONT_SIZE)
        self.MENU_WIDTH = self.window_dimensions.width * MenuDimensions.MENU_WIDTH_RATIO
        self.ITEM_HEIGHT = self.window_dimensions.height * MenuDimensions.MENU_ITEM_HEIGHT_RATIO
        self.menu_activator = MenuActivator()

    def build_menu_bar(self):        
        self.menu_bar = MenuBar(self.window_dimensions.width, self.MENU_BAR_HEIGHT, MenuDimensions.MENU_ITEM_SPACING, 
                                MenuColorConfig.MENUBAR_BG)
        self.menu_bar.add_supported_events([pygame.MOUSEBUTTONDOWN])   

    def build(self):
        # Create "File" menu
        self.build_menu_bar()
        self.build_all_menus(self.MENU_BAR_HEIGHT)
        return self.menu_bar
    
    def build_all_menus(self, menu_bar_height):             
        self.menu_bar.add_menu(self._create_menu("File", menu_bar_height, self.ITEM_HEIGHT, MenuItemsData.FILE))
        self.menu_bar.add_menu(self._create_menu("EDIT", menu_bar_height, self.ITEM_HEIGHT, MenuItemsData.EDIT))

    def _create_menu(self, title, menu_bar_height, item_height, items):
        """Helper method to create a dropdown menu with common styling."""        
        menu = DropdownMenu(
            self.menu_activator, title, self.MENU_WIDTH, menu_bar_height, item_height,
            MenuColorConfig.MENU_HOVER, MenuColorConfig.MENU_BG, 
            self.BIG_FONT, self.SMALL_FONT,
            MenuColorConfig.DROP_BG, MenuColorConfig.DROP_HOVER, 
            MenuColorConfig.BORDER, MenuColorConfig.SHADOW, 
            MenuDimensions.MENU_RADIUS,
            text_color=MenuColorConfig.TEXT_COLOR
        )
        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, menu)
        menu.add_supported_events([pygame.MOUSEBUTTONDOWN])
        self.build_menu_items(menu, items)
        return menu
   
    def build_menu_items(self, menu, item_details):
        item_width = MenuDimensions.MENU_ITEM_WIDTH_RATIO * self.MENU_WIDTH
         
        for item in item_details:
            text, action = item[:2]
            key_shortcut = item[2] if len(item) > 2 else None
            rect = pygame.Rect(0, 0, item_width, self.ITEM_HEIGHT)
            item = DropDownMenuItem(self.menu_activator, text, action, rect,
                                    text_color=MenuColorConfig.TEXT_COLOR,
                                    bg_color=MenuColorConfig.MENU_BG,
                                    hover_text_color=MenuColorConfig.MENU_ITEM_HOVER_TEXT_COLOR,
                                    hover_bg_color=MenuColorConfig.MENU_ITEM_HOVER_BG,
                                    border_radius=MenuDimensions.MENU_RADIUS,
                                    font=self.SMALL_FONT, key_shortcut=key_shortcut)
            
            self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, item)
            self.event_handler.subscribe(pygame.MOUSEBUTTONUP, item)
            self.event_handler.subscribe(pygame.KEYDOWN, item)
            item.add_supported_events([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN])

            menu.add_item(item)