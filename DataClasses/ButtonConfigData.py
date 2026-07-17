

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

class StaffActionIdentifiers(Enum):
    ADD_STAFF_ACTION= auto()
    DELETE_STAFF_ACTION= auto()
    CREATE_GRAND_STAFF_ACTION=auto()
    EXTEND_GRAND_STAFF_ACTION=auto()

@dataclass
class ActionButtonConfig:
    Id: StaffActionIdentifiers
    name: str
    tooltip: str
    action: str
    icon_path: str
    position: StaffActionButtonPosition
    visible: bool
    ignore_previous_offset_x: bool | None = None
    ignore_previous_offset_y: bool | None = None
    size: Size=Size(20,20)
   
@dataclass
class StaffActionButtonConfig:
    Position: StaffActionButtonPosition
    ConfigIds: list[StaffActionIdentifiers]

# Icons are from this site: https://www.flaticon.com/search?word=Add
STAFF_ACTION_BUTTON_CONFIG = [
    ActionButtonConfig(
        Id=StaffActionIdentifiers.ADD_STAFF_ACTION,
        name="Staff Add",
        tooltip="Add staff",
        action="duplicate_staff_below",
        icon_path="add.png",
        position=StaffActionButtonPosition.RIGHT,
        visible = True
    ),
    ActionButtonConfig(
        Id=StaffActionIdentifiers.DELETE_STAFF_ACTION,
        name="Staff Delete",
        tooltip="Delete staff",
        action="confirm_delete",
        icon_path="red-bin.png",
        position=StaffActionButtonPosition.RIGHT,
        visible = True
    ),
    ActionButtonConfig(
        Id=StaffActionIdentifiers.CREATE_GRAND_STAFF_ACTION,
        name="Create Grand Staff",
        tooltip="Convert to grand staff",
        action="convert_to_grand_staff",
        icon_path="create-grand-staff.png",
        position=StaffActionButtonPosition.RIGHT,
        visible = True,
        size = Size(20,33)
    ),
    ActionButtonConfig(
        Id=StaffActionIdentifiers.EXTEND_GRAND_STAFF_ACTION,
        name="Extent Grand Staff",
        tooltip="Extend grand staff",
        action="extend_grand_staff",
        icon_path="x-grand-staff.png",
        position=StaffActionButtonPosition.RIGHT,
        visible = False,
        ignore_previous_offset_y = True,
        size = Size(20,40)
    )
]

    