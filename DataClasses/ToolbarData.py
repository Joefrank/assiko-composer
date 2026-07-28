from dataclasses import dataclass

import pygame

from DataClasses.ButtonData import ButtonType
from DataClasses.Config import ScreenConfig
from DataClasses.Config.MusicConfig import BASS_CLEF, TREBLE_CLEF, AccidentalOptions, NoteDurationInTicks
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
    FONT = (ScreenConfig.FontConfig.NOTO_SANS_SYMBOLS2_REGULAR, 14)
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
        ("\U0001D15D","Whole", NoteDurationInTicks.WHOLE),  # Whole
        ("\U0001D15E","Half", NoteDurationInTicks.HALF),  # Half
        ("\U0001D15F","Quarter", NoteDurationInTicks.QUARTER),  # Quarter
        ("\U0001D160","Eighth", NoteDurationInTicks.EIGHT),  # Eighth
        ("\U0001D161","Sixteenth", NoteDurationInTicks.SIXTHEENTH),  # Sixteenth
        ("\U0001D162","Thirty-second", NoteDurationInTicks.THIRTYSECONDTH),
        ("\U0001D163","Sixty-fourth", NoteDurationInTicks.SIXTYFOURTH)
    ]   
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.BOTTOM_CENTER
    DROP_ACTION = "PositionNoteOnStaff"
 
@dataclass
class RestToolbar(BaseToolbar):
    NAME = "RestToolbar"
    ICONS =[
        ("\U0001D13B","Whole",  NoteDurationInTicks.WHOLE),  # Whole
        ("\U0001D13C","Half", NoteDurationInTicks.HALF),  # Half
        ("\U0001D13D","Quarter", NoteDurationInTicks.QUARTER),  # Quarter
        ("\U0001D13E","Eighth", NoteDurationInTicks.EIGHT),  # Eighth
        ("\U0001D13F","Sixteenth", NoteDurationInTicks.SIXTHEENTH),  # Sixteenth
        ("\U0001D140","32nd", NoteDurationInTicks.THIRTYSECONDTH),  # 32nd
        ("\U0001D141","64th", NoteDurationInTicks.SIXTYFOURTH),  # 64th
        #("\U0001D142","128th"),  # 128th
    ]
    DROP_ACTION = "PositionRestOnStaff"

@dataclass
class AccidentalsToolbar(BaseToolbar):
    NAME: str = "AccidentalsToolbar"
    ICONS = [
        ("\uE262", "SHARP", AccidentalOptions.SHARP),  # SHARP
        ("\uE260", "FLAT", AccidentalOptions.FLAT),  # FLAT
        ("\uE261", "NATURAL", AccidentalOptions.NATURAL),   # NATURAL
        ("\uE263", "DOUBLE_SHARP", AccidentalOptions.DOUBLE_SHARP),   # DOUBLE_SHARP
        ("\uE264", "DOUBLE_FLAT", AccidentalOptions.DOUBLE_FLAT)   # DOUBLE_FLAT
    ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 25)
    DROP_ACTION = "PositionAccidental"

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
    DROP_ACTION = "PositionTimeSignature"

@dataclass
class CommonTimeSignatureToolbar(BaseToolbar):
    NAME: str = "CommonTimeSignatureToolbar"
    ICONS =[
                ("\uE08A", "Common Time","4x4"),
                ("\uE08B", "Cut Time", "2x2")                             
            ]
    DROP_ACTION = "PositionTimeSignature"

@dataclass
class KeySignatureToolbar(BaseToolbar):
    NAME: str = "KeySignatureToolbar"
    ICONS =[
                (("\uE262",1), "G MAJOR", "G"),
                (("\uE262",2), "D MAJOR", "D"),
                (("\uE262",3), "A MAJOR", "A"),
                (("\uE262",4), "E MAJOR", "E"),
                (("\uE262",5), "B MAJOR", "B"),
                (("\uE262",6), "F# MAJOR", "F#"),
                (("\uE262",7), "C# MAJOR", "C#"),           
            ]
    BUTTON_TYPE = ButtonType.STAGGERED_SYMBOL_BUTTON
    DROP_ACTION = "PositionKeySignature"

@dataclass
class DynamicsToolbar(BaseToolbar):
    NAME: str = "DaynamicsToolbar"
    ICONS = [
        ("\uE52D", "mf"),
        ("\uE52C", "mp"),
        ("\uE522", "f"),
        ("\uE520", "p"),
        ("\uE52F", "ff"),
        ("\uE52A", "pp"),
        ("\uE530", "fff"),
        ("\uE52B", "ppp"),
        ("\uE539", "sfz"),
        ("\uE537", "sf"),
        ("\uE535", "fz"),
        ("\uE534", "fp"),
        ("\uE536", "rf"),
        ("\uE53E", "crescendo"),
        ("\uE53F", "diminuendo"),
    ]
    DROP_ACTION = "PositionDynamic"

@dataclass
class ClefToolbar(BaseToolbar):
    NAME: str = "ClefToolbar"
    ICONS =[
                ("\uE050", "TREBLE CLEF", "PositionClef", TREBLE_CLEF),
                ("\uE062", "BASS CLEF", "PositionClef", BASS_CLEF)
            ]
    DROP_ACTION = "PositionClef"

@dataclass
class StaffActionToolbar(BaseToolbar):
    NAME: str = "StaffActionToolbar"
    ICONS = [
        ("music_staff.png", "Music Staff", "CreateStaff"),
        ("repeat_start.png", "Repeat Start", "InsertStartRepeatToStaff"),
        ("repeat_end.png", "Repeat End", "InsertEndRepeatToStaff"),
        ("final_staff_line.png", "Final Staff Line", "InsertFinalStaffLine"),
        ("notes_tie.png", "Notes Tie", "TieNotesOnStaff") ,
        ("text.png", "Text Input", "CreateTextInput"),       
    ]
    BUTTON_TYPE = ButtonType.IMAGE_BUTTON
    DROP_ACTION = "Reflect"
    
TOOLBAR_MATRIX = [
    [NotesToolbar, AccidentalsToolbar, PlayToolbar, KeySignatureToolbar],
    [RestToolbar, TimeSignatureToolbar, CommonTimeSignatureToolbar, ClefToolbar, StaffActionToolbar]
]

@dataclass
class ToolbarGridConfig:
    GRID_SPACING = (5, 5)
    GRID_ROWS = 2
    GRID_COLS = 4
    GRID_NAME = "Horizontal_ToolbarGrid"