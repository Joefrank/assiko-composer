from dataclasses import dataclass

import pygame

from DataClasses.Config import ScreenConfig
from Model.Position import TextPosition

@dataclass
class ToolbarDimensions:
    BUTTON_WIDTH = 40
    BUTTON_HEIGHT = 30
    BUTTON_MARGIN = 10
    BUTTON_BORDER_RADIUS = 6
    TOP_OFFSET_RATIO = 0.1
    TOOLBAR_HEIGHT_RATIO = 0.06
    TOOLBAR_ITEM_HEIGHT_RATIO = 0.038
    TOOLBAR_ITEM_WIDTH_RATIO = 0.025
    DEFAULT_TOOLBAR_WIDTH = 10
    TOOLBAR_SPACING = 20

@dataclass
class PlayToolbar:
    NAME = "PlayToolbar"
    ICONS = [  
        ("⏮", "Previous"),     
        ("▶", "Play"),
        ("⏸", "Pause"),
        ("⏹", "Stop"),
        ("⏭", "Next"),
         
    ]
    FONT = ("Segoe UI Symbol", 14)
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    BUTTON_BG_COLOR = (70, 70, 70)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (100, 100, 100)
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.CENTER
    DRAGGABLE_BUTTONS = False
    SUPPORTED_EVENTS = [pygame.MOUSEMOTION]

@dataclass
class NotesToolbar:
    NAME = "NotesDurationToolbar"
    ICONS =[
        ("\U0001D15D","Whole"),  # Whole
        ("\U0001D15E","Half"),  # Half
        ("\U0001D15F","Quarter"),  # Quarter
        ("\U0001D160","Eighth"),  # Eighth
        ("\U0001D161","Sixteenth"),  # Sixteenth
        ("\U0001D162","Thirty-second"),
        ("\U0001D163","Sixty-fourth")
    ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 18)
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (25, 25, 25)
    BUTTON_BG_COLOR = (255, 200, 200)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (200, 180, 180)
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.BOTTOM_CENTER
    DRAGGABLE_BUTTONS = True
    SUPPORTED_EVENTS = [pygame.MOUSEMOTION]

@dataclass
class RestToolbar:
    NAME = "RestToolbar"
    ICONS =[
        ("\U0001D13B","Whole"),  # Whole
        ("\U0001D13C","Half"),  # Half
        ("\U0001D13D","Quarter"),  # Quarter
        ("\U0001D13E","Eighth"),  # Eighth
        ("\U0001D13F","Sixteenth"),  # Sixteenth
        ("\U0001D140","32nd"),  # 32nd
        ("\U0001D141","64th"),  # 64th
        ("\U0001D142","128th"),  # 128th
    ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 18)
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (25, 25, 25)
    BUTTON_BG_COLOR = (255, 200, 200)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (200, 180, 180)
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.CENTER
    DRAGGABLE_BUTTONS = True
    SUPPORTED_EVENTS = [pygame.MOUSEMOTION]

@dataclass
class ToolbarGridConfig:
    GRID_SPACING = (10, 10)
    GRID_ROWS = 2
    GRID_COLS = 3
    GRID_NAME = "Horizontal_ToolbarGrid"