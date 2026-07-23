from dataclasses import dataclass
from enum import Enum
from typing import Tuple

class ScoreNavigatorStatus(Enum):
    INVACTIVE = 1,
    RUNNING = 2,
    PAUSE = 3

@dataclass
class Color:
    BLACK = (25,25,25)
    RED = (255,0,0)
    GREY = (100,100,100)
    LIGHT_GRAY = (150,150,150)
    BLUE = (25, 25, 255)
    SKYBLUE = (144,212,255)
    WHITE = (255,255,255)
    PINK = (255, 192, 203)

@dataclass
class MouseEventType:
    CLICK = "click"
    HOVER = "hover"

@dataclass
class WindowConfig:
    """Window configuration settings."""
    WIDTH: int = 1200
    HEIGHT: int = 800
    CAPTION: str = "AI Piano Music Board"
    BACKGROUND_COLOR: Tuple[int, int, int] = (250, 250, 250)
    RESIZABLE: bool = True

#background_color, width, height, item_width, item_height
@dataclass
class MainMenuConfig:
    BACKGROUND_COLOR = Color.SKYBLUE
    WIDTH = WindowConfig.WIDTH
    HEIGHT = 50
    PADDING = 10

@dataclass
class SubMenuConfig:
    BACKGROUND_COLOR = Color.WHITE
    HEIGHT = 50
    
@dataclass
class MenuItemConfig:
    WIDTH = 150
    HEIGHT = MainMenuConfig.HEIGHT - 16
    BACKGROUND_COLOR = Color.BLUE
    TEXT_COLOR = Color.WHITE
    HOVER_COLOR = Color.PINK
    SELECTED_COLOR = Color.RED
    FONT_SIZE = 30

@dataclass
class StaffConfig:
    """Staff configuration settings."""
    STAFF_WIDTH_PERCENT: int = 90 # this is a percentage
    STAFF_LINE_GAP: int = 10
    STAFF_LINE_THICKNESS: int = 1
    STAFF_BAR_THICKNESS: int = 2
    STAFF_SPACING: int = 80  # space between two staves within grandstaff
    GRAND_STAFF_ORIGINAL_SPACING = 100
    GRAND_STAFF_SUBSEQUENT_SPACING = 50
    STAFF_CLEF_LEFT: int =  20
    STAFF_NO_LINES: int =  5
    STAFF_NO_INTERVALS: int =  4
    STAFF_RIGHT_PADDING:  int = 10
    STAFF_LEFT_PADDING: int = 1 # use as default only for empty staff when clef is not added yet.
    STAFF_ALLOWED_MARGIN: int =  55
    STAFF_NOTE_SIZE:  int = 40
    STAFF_ACCIDENTAL_SIZE: int = 30
    STAFF_NOTE_SPACE: int = 100
    STAFF_NOTE_STEM_SIZE: int =  30
    STAFF_ORIGINAL_Y_OFFSET: int = 200 # this is where the first staff will be placed. all subsequent will be calculated from this
    VIRTUAL_LINE_WIDTH:  int = 20
    STAFF_ITEM_THRESHOLD: int = 2
    STACCATO_SYMBOL_SIZE: int = 40
    NOTE_PROXIMITY_THRESHOLD: int = 40

@dataclass
class ScoreConfig:
    SCORE_WIDTH_PERCENT: int = 90 # this is a percentage
    HEADER_FONT_SIZE: int = 30
    TITLE_Y_OFFSET: int = 30


@dataclass
class FontConfig:
    BRAVURA_FONT_PATH = "Assets/Fonts/Bravura.otf"
    NOTOSANS_FONT_PATH = "Assets/Fonts/NotoSansAdlam-Regular.otf"
    NOTO_SERIFAHOM_REGULAR_FULL = "Assets/Fonts/NotoSerifAhom-Regular Full.ttf"
    NOTO_SANADLAM_REGULAR = "Assets/Fonts/NotoSansAdlam-Regular.ttf"
    NOTO_SERIFAHOM_REGULAR = "Assets/Fonts/NotoSerifAhom-Regular.ttf"
    NOTO_SANS_SYMBOLS2_REGULAR = "Assets/Fonts/NotoSansSymbols2-Regular.ttf"
    
staff_generic_settings = {
    "STAFF_LINE_GAP": 10,
    "STAFF_LINE_THICKNESS": 1,
    "STAFF_SPACING": 160, # space between two staves within grandstaff
    "STAFF_CLEF_LEFT": 20,
    "STAFF_NO_LINES": 5,
    "STAFF_NO_INTERVALS": 4,
    "STAFF_RIGHT_PADDING": 10,
    "STAFF_ALLOWED_MARGIN": 50,
    "STAFF_NOTE_SIZE": 40,
    "STAFF_NOTE_STEM_SIZE": 30,
    "VIRTUAL_LINE_WIDTH": 20,
    "MODULATION_FONT_SIZE": 30,
    "TIME_SIGNATURE_FONT_SIZE": 35,
}

@dataclass
class SupportedLanguages:
    ENGLISH = "enGB"
    FRENCH = "frFR"  

score_font_size ={
    "HEADER_FONT_SIZE": 40,
}

VERTICAL_POSITION_TOP = -1
VERTICAL_POSITION_ON = 0
VERTICAL_POSITION_BOTTOM = 1
