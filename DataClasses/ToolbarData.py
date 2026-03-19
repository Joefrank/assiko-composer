from dataclasses import dataclass

import pygame

from DataClasses.ButtonData import ButtonType
from DataClasses.Config import ScreenConfig
from DataClasses.ControlData import ControlType
from Model.Geometry.Position import TextPosition

@dataclass
class ToolbarDimensions:
    BUTTON_WIDTH = 40
    BUTTON_HEIGHT = 30
    BUTTON_MARGIN = 5
    BUTTON_BORDER_RADIUS = 6
    TOP_OFFSET_RATIO = 0.1
    TOOLBAR_HEIGHT_RATIO = 0.06
    TOOLBAR_ITEM_HEIGHT_RATIO = 0.038
    TOOLBAR_ITEM_WIDTH_RATIO = 0.025
    DEFAULT_TOOLBAR_WIDTH = 10
    TOOLBAR_SPACING = 20

@dataclass
class BaseToolbar:
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (25, 25, 25)
    BUTTON_BG_COLOR = (255, 200, 200)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (200, 180, 180)
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.CENTER
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 18)
    DRAGGABLE_BUTTONS = True # TODO: rename to draggable_symbols, as it makes more sense
    SUPPORTED_EVENTS = [pygame.MOUSEMOTION]
    BUTTON_TYPE = ButtonType.BUTTON

@dataclass
class PlayToolbar(BaseToolbar):
    NAME = "PlayToolbar"
    ICONS = [  
        ("⏮", "Previous"),     
        ("▶", "Play"),
        ("⏸", "Pause"),
        ("⏹", "Stop"),
        ("⏭", "Next")         
    ]
    FONT = ("Segoe UI Symbol", 14)
    DRAGGABLE_BUTTONS = False
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    BUTTON_BG_COLOR = (70, 70, 70)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (100, 100, 100)

@dataclass
class NotesToolbar(BaseToolbar):
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
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.BOTTOM_CENTER
 
@dataclass
class RestToolbar(BaseToolbar):
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

@dataclass
class AccidentalsToolbar(BaseToolbar):
    NAME: str = "AccidentalsToolbar"
    ICONS = [
        ("\uE262", "SHARP"),  # SHARP
        ("\uE260", "FLAT"),  # FLAT
        ("\uE261", "NATURAL"),   # NATURAL
        ("\uE263", "DOUBLE_SHARP"),   # DOUBLE_SHARP
        ("\uE264", "DOUBLE_FLAT")   # DOUBLE_FLAT
    ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 25)

@dataclass
class TimeSignatureToolbar(BaseToolbar):
    NAME: str = "TimeSignatureToolbar"
    ICONS =[
                ((chr(0xE082),chr(0xE082)),"2x2"), 
                ((chr(0xE082),chr(0xE084)),"2x4"),
                ((chr(0xE083),chr(0xE082)),"3x2"),
                ((chr(0xE083),chr(0xE084)),"3x4"),
                ((chr(0xE084),chr(0xE084)),"4x4"),
                ((chr(0xE086), chr(0xE088)),"6x8"),
                ((chr(0xE089), chr(0xE088)),"9x8"),
                ((chr(0xE081) + chr(0xE082), chr(0xE088)),"12x8")
            ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 18)   
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.BOTTOM_CENTER   
    BUTTON_TYPE = ButtonType.TIME_SIGNATURE_BUTTON

@dataclass
class CommonTimeSignatureToolbar(BaseToolbar):
    NAME: str = "CommonTimeSignatureToolbar"
    ICONS =[
                ("\uE08A", "Common Time"),
                ("\uE08B", "Cut Time")                             
            ]

@dataclass
class ClefToolbar(BaseToolbar):
    NAME: str = "ClefToolbar"
    ICONS =[
                ("\uE050", "G_CLEF"),
                ("\uE062", "F_CLEF"),
                ("\uE05C", "C_CLEF")                
            ]

@dataclass
class KeySignatureToolbar(BaseToolbar):
    NAME: str = "KeySignatureToolbar"
    ICONS =[
                (("\uE262",1), "G MAJOR"),
                (("\uE262",2), "D MAJOR"),
                (("\uE262",3), "A MAJOR"),
                (("\uE262",4), "E MAJOR"),
                (("\uE262",5), "B MAJOR"),
                (("\uE262",6), "F# MAJOR"),
                (("\uE262",7), "C# MAJOR"),           
            ]
    BUTTON_TYPE = ButtonType.STAGGERED_SYMBOL_BUTTON


TOOLBAR_MATRIX = [
    [NotesToolbar, AccidentalsToolbar, PlayToolbar, KeySignatureToolbar],
    [RestToolbar, TimeSignatureToolbar, CommonTimeSignatureToolbar, ClefToolbar]
]

@dataclass
class ToolbarGridConfig:
    GRID_SPACING = (5, 5)
    GRID_ROWS = 2
    GRID_COLS = 4
    GRID_NAME = "Horizontal_ToolbarGrid"