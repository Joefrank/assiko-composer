

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
    action_params: Any = None
    

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


class ActionButtonPosition(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()

class ActionIdentifiers(Enum):
    ADD_STAFF_ACTION= auto()
    DELETE_STAFF_ACTION= auto()
    CREATE_GRAND_STAFF_ACTION=auto()
    EXTEND_GRAND_STAFF_ACTION=auto()
    ADD_TEXT_ITEM_ACTION=auto()
    DELETE_TEXT_ITEM_ACTION=auto()
    INCREASE_TEXT_SIZE = auto()
    DECREASE_TEXT_SIZE= auto()   
    TOGGLE_FONT_BOLD= auto()
    TOGGLE_ITALIC = auto()

@dataclass
class ActionButtonConfig:
    Id: ActionIdentifiers
    name: str
    tooltip: str
    action: str
    icon_path: str
    position: ActionButtonPosition
    visible: bool
    ignore_previous_offset_x: bool | None = None
    ignore_previous_offset_y: bool | None = None
    alternate_icon_path: str | None = None
    size: Size=Size(20,20)
   
@dataclass
class ActionButtonGroupConfig:
    Position: ActionButtonPosition
    ConfigIds: list[ActionIdentifiers]

# Icons are from this site: https://www.flaticon.com/search?word=Add

STAFF_ACTION_BUTTON_CONFIG = [
    ActionButtonConfig(
        Id=ActionIdentifiers.ADD_STAFF_ACTION,
        name="Staff Add",
        tooltip="Add staff",
        action="duplicate_staff_below",
        icon_path="add.png",
        position=ActionButtonPosition.RIGHT,
        visible = True
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.DELETE_STAFF_ACTION,
        name="Staff Delete",
        tooltip="Delete staff",
        action="confirm_delete",
        icon_path="red-bin.png",
        position=ActionButtonPosition.RIGHT,
        visible = True
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.CREATE_GRAND_STAFF_ACTION,
        name="Create Grand Staff",
        tooltip="Convert to grand staff",
        action="convert_to_grand_staff",
        icon_path="create-grand-staff.png",
        position=ActionButtonPosition.RIGHT,
        visible = True,
        size = Size(20,33)
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.EXTEND_GRAND_STAFF_ACTION,
        name="Extent Grand Staff",
        tooltip="Extend grand staff",
        action="extend_grand_staff",
        icon_path="x-grand-staff.png",
        position=ActionButtonPosition.RIGHT,
        visible = False,
        ignore_previous_offset_y = True,
        size = Size(20,40)
    )
]

TEXT_ITEM_ACTION_BUTTON_CONFIG = [
    ActionButtonConfig(
        Id=ActionIdentifiers.INCREASE_TEXT_SIZE,
        name="Text Size Increase",
        tooltip="Increase size",
        action="increase_text_size",
        icon_path="text_size_inc.png",
        position=ActionButtonPosition.TOP,
        visible=True           
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.DECREASE_TEXT_SIZE,
        name="Text Size Decrease",
        tooltip="Decrease size",
        action="decrease_text_size",
        icon_path="text_size_dec.png",
        position=ActionButtonPosition.TOP,
        visible=True           
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.TOGGLE_FONT_BOLD,
        name="Toggle font bold",
        tooltip="Toggle font bold",
        action="toggle_font_bold",
        icon_path="bold_on.png",
        alternate_icon_path = "bold_off.png",
        position=ActionButtonPosition.TOP,
        visible=True           
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.TOGGLE_ITALIC,
        name="Toggle italic bold",
        tooltip="Toggle italic bold",
        action="toggle_font_italic",
        icon_path="italic_on.png",
        alternate_icon_path = "italic_off.png",
        position=ActionButtonPosition.TOP,
        visible=True           
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.ADD_TEXT_ITEM_ACTION,
        name="Text Item Add",
        tooltip="Add text item",
        action="add_text_item_below",
        icon_path="add.png",
        position=ActionButtonPosition.TOP,
        visible=True       
    ),
    ActionButtonConfig(
        Id=ActionIdentifiers.DELETE_TEXT_ITEM_ACTION,
        name="Text Item Delete",
        tooltip="Delete text item",
        action="confirm_delete",
        icon_path="red-bin.png",
        position=ActionButtonPosition.TOP,
        visible=True
    )
]

    