import pygame
from dataclasses import dataclass

@dataclass 
class MenuColorConfig:
    MENUBAR_BG = (105, 105, 105)
    MENU_BG = (50, 50, 70)
    MENU_HOVER = (75, 75, 75)
    TEXT_COLOR = (235, 235, 235)
    DROP_BG = (55, 55, 55)
    DROP_HOVER = (95, 95, 95)
    BORDER = (110, 110, 110)
    SHADOW = (0, 0, 0, 90)
    MENU_ITEM_HOVER_BG = (80, 80, 80)
    MENU_ITEM_HOVER_TEXT_COLOR = (255, 255, 255)


@dataclass
class MenuFontConfig:
    BIG_FONT_SIZE = 16
    SMALL_FONT_SIZE = 14

@dataclass
class MenuDimensions:
    MENU_BAR_HEIGHT_RATIO = 0.07
    MENU_HEIGHT_RATIO =  0.6 #relative to menu bar height
    MENU_WIDTH_RATIO = 0.09
    MENU_ITEM_SPACING = 10
    MENU_ITEM_HEIGHT_RATIO = 0.05
    MENU_ITEM_WIDTH_RATIO = 0.95 #ratio to dropdown menu width
    MENU_ITEM_RADIUS = 6
    MENU_RADIUS = 8

@dataclass
class MenuItemsData:
    FILE = [
                ("New   Ctrl+N", "new_file", pygame.K_n),
                ("Open  Ctrl+O", "open_file", pygame.K_o),
                ("Save  Ctrl+S", "save_file", pygame.K_s),
                ("Exit  Ctrl+Q", "exit_app", pygame.K_q)
            ]    
    EDIT = [
                ("Undo Ctrl+Z", "undo_last_action", pygame.K_z),
                ("Redo Ctrl+Y", "redo_last_action", pygame.K_y),
           ]
