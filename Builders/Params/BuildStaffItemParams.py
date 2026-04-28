

from dataclasses import dataclass

from DataClasses.Config.ScreenConfig import VERTICAL_POSITION_ON, StaffConfig
from Model.Control import Control
from Model.Geometry.Position import Position
from Model.Score.Staff import Staff


@dataclass
class StaffItemBuildParams:
    no_of_items:int
    staff_width:int
    original_position:Position
    parent_staff:Staff
    line_thickness:int=StaffConfig.STAFF_LINE_THICKNESS
    interval_thickness:int=StaffConfig.STAFF_LINE_GAP    
    is_virtual:bool=False
    vertical_positioning:int=VERTICAL_POSITION_ON
    left_collateral_offset:int=StaffConfig.STAFF_LEFT_PADDING
    right_collateral_offset:int=StaffConfig.STAFF_RIGHT_PADDING    
    piano_key_details: tuple = tuple()
    key=None
    key_id=None
    velocity: int = None
    tempo: int = None


@dataclass
class EmptyStaffBuildParams:
    original_position:Position
    container:Control
    line_thickness:int
    interval_thickness:int
    staff_vertical_margin:int
    staff_width_percentage:int
    staff_right_padding:int
    staff_left_padding:int


# StaffConfig.STAFF_ALLOWED_MARGIN, staff_with,
#                                                            StaffConfig.STAFF_LINE_GAP,
#                                                            StaffConfig.STAFF_LINE_THICKNESS,
#                                                            StaffConfig.STAFF_SPACING,
#                                                            StaffConfig.STAFF_NO_LINES,
#                                                            StaffConfig.STAFF_NO_INTERVALS