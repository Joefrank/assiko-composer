

from dataclasses import dataclass

from DataClasses.Config.ScreenConfig import StaffConfig
from Model.Geometry.Position import Position
from Model.Score.Staff import Staff


@dataclass
class BuildStaffItemParams:
    no_of_items:int
    line_thickness:int
    interval_thickness:int
    original_position:Position
    is_virtual:bool
    vertical_positioning:int
    left_collateral_offset:int
    right_collateral_offset:int #= StaffConfig.STAFF_RIGHT_PADDING
    parent_staff:Staff
    piano_key_details: tuple


# StaffConfig.STAFF_ALLOWED_MARGIN, staff_with,
#                                                            StaffConfig.STAFF_LINE_GAP,
#                                                            StaffConfig.STAFF_LINE_THICKNESS,
#                                                            StaffConfig.STAFF_SPACING,
#                                                            StaffConfig.STAFF_NO_LINES,
#                                                            StaffConfig.STAFF_NO_INTERVALS