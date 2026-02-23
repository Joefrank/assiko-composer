from dataclasses import dataclass

@dataclass
class MainWindowDimensions:
    WIDTH_RATIO: float = 0.9
    HEIGHT_RATIO: float = 0.85

@dataclass
class MainWindowText:
    TITLE: str = "AI Music Notation Editor"

@dataclass
class MainWindowConfig:
    LEFT_PADDING_RATIO= 0.1
    MAIN_CONTAINER_WIDTH_RATIO = 0.8

@dataclass
class ControlZIndex:
    BACKGROUND = 0
    LEVEL1 = 1 #MAIN CONTAINER, 
    LEVEL2 = 2 #TOOLBARS
    LEVEL3 = 3 #MENUES, 
    LEVEL4 = 4 #STATUSBAR