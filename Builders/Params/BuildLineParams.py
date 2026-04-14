

from dataclasses import dataclass

from DataClasses.Config.ScreenConfig import StaffConfig
from Model.Geometry.Position import Position
from Model.Score.Staff import Staff


@dataclass
class BuildEmptyIntervalsParams:
    no_of_lines:int
    interval_thickness:int
    line_thickness:int
    original_position:Position
    is_virtual:bool
    vertical_positioning:int
    left_collateral_offset:int
    right_collateral_offset:int = StaffConfig.STAFF_RIGHT_PADDING
    parent_staff:Staff
    piano_key_details: tuple

# no_of_lines, 
# interval_thickness, 
# line_thickness, 
# piano_key_details, 
# original_position, 
# is_virtual, 
# vertical_positioning,
# left_collateral_offset,
# right_collateral_offset