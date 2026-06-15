

from dataclasses import dataclass, field
from typing import Any

from pygame import Rect
from enum import Enum, auto
from Model.Geometry.Size import Size
from Model.Toolbars.Toolbar import Toolbar


@dataclass
class ButtonConfig:
    screen: Any
    toolbar: Toolbar
    action: str
    icon: str
    font: Any
    font_details: tuple
    border_radius: int = 0
    text_color: tuple = (250, 250, 250)
    bg_color: tuple = (50, 50, 50) 
    hover_text_color: tuple = (250, 250, 250) 
    hover_bg_color: tuple = (100, 100, 100)
    draggable_icons: bool = False
    position: tuple = (0,0)
    symbols: list = field(default_factory=list)
    action_value: Any = None
    

@dataclass
class SimpleButtonParams:
    screen: Any 
    action: str
    rect: Rect 
    icon: str   
    font: Any 
    font_details: tuple
    button_text_center: tuple
    text_color: tuple
    bg_color: tuple
    hover_text_color: tuple 
    hover_bg_color: tuple      
    border_radius: int = 0 
    draggable_icons=[] 
    action_value=None


class StaffActionButtonPosition(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()

@dataclass
class ActionButtonConfig:
    name: str
    tooltip: str
    action: str
    icon_path: str
    position: StaffActionButtonPosition
    size: Size=Size(20,20)

# Icons are from this site: https://www.flaticon.com/search?word=Add
STAFF_ACTION_BUTTON_CONFIG = [
    ActionButtonConfig(
        name="Staff Add",
        tooltip="Add staff",
        action="AddStaff",
        icon_path="add.png",
        position=StaffActionButtonPosition.RIGHT
    ),
    ActionButtonConfig(
        name="Staff Delete",
        tooltip="Delete staff",
        action="DeleteStaff",
        icon_path="red-bin.png",
        position=StaffActionButtonPosition.RIGHT
    )
]

    