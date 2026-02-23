from enum import Enum, auto

class ControlType(Enum):
    MENUITEM = auto()
    MENU = auto()
    MENUBAR = auto()
    TOOLBAR = auto()
    TOOLBARITEM = auto()
    CONTAINER = auto()
    WINDOW = auto()

