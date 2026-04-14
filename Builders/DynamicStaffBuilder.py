
"""
    Class is used to build staff progressively while user creates it and adds items to it.
"""
from Builders.Params.BuildStaffItemParams import BuildEmptyIntervalsParams, BuildStaffItemParams
from DataClasses.Config.ScreenConfig import StaffConfig
from Model.Geometry.Position import Position
from Model.Score import StaffLine
from Model.Score.CollateralBoundary import CollateralBoundary
from Model.Score.Interval import Interval
from Model.Score.Rect import Rect
from Model.Score.Staff import Staff


class DynamicStaffBuilder:

    def __init__(self, container):        
        self.container = container
        # work out first staff position and width
        self.staff_with, self.staff_original_position = self.calculate_first_staff_position(container,
                                                                                      StaffConfig.STAFF_WIDTH_PERCENT,
                                                                                      StaffConfig.STAFF_ORIGINAL_Y_OFFSET)
       
    def build_empty_staff(self, position:Position):
        staff = Staff()
        self.build_virtual_intervals(self.interval_thickness, self.line_thickness, top_notes.interval_notes, 
                                                   original_position, VERTICAL_POSITION_TOP, possible_no_oftop_lines_and_intervals,
                                                   staff_left_x_offset, StaffConfig.STAFF_RIGHT_PADDING)
        # Build all lines and intervals on staff
        original_position = staff_original_position
        #print(f"original_position Lines: {original_position.x, original_position.y}")
        self.staff_builder.build_lines(self.staff_no_lines, self.interval_thickness, self.line_thickness, staff_notes.line_notes,
                                       original_position, False, VERTICAL_POSITION_ON, staff_left_x_offset, StaffConfig.STAFF_RIGHT_PADDING)
        original_position = Position(staff_original_position.x, staff_original_position.y + self.line_thickness)
        # print(f"original_position Intervals: {original_position.x, original_position.y}")
        self.staff_builder.build_intervals(self.staff_no_intervals, self.interval_thickness, self.line_thickness, staff_notes.interval_notes,
                                           original_position, False, VERTICAL_POSITION_ON, staff_left_x_offset, StaffConfig.STAFF_RIGHT_PADDING)
        # Build all lines and intervals below the staff
        staff_bottom_line = self.staff_builder.get_staff_bottom_line()
        #staff_bottom_line = self.staff_builder.staff.bottom_line # we can now use the staff bottom_line
        original_position = Position(staff_bottom_line.start_position.x, staff_bottom_line.start_position.y + 1) # + 1 because we want to start at the next pixel after the bottom line thickness
        
        self.staff_builder.build_virtual_intervals(self.interval_thickness, self.line_thickness, bottom_notes.interval_notes, 
                                                   original_position, VERTICAL_POSITION_BOTTOM, possible_no_oftop_lines_and_intervals,
                                                     staff_left_x_offset, StaffConfig.STAFF_RIGHT_PADDING)
        original_position = Position(staff_bottom_line.start_position.x, staff_bottom_line.start_position.y + self.interval_thickness + 1)
       # print(f"original_position VL-bottom: {original_position.x, original_position.y}")
        self.staff_builder.build_virtual_lines(self.interval_thickness, self.line_thickness, bottom_notes.line_notes, original_position,
                                               VERTICAL_POSITION_BOTTOM, possible_staff_padding, possible_no_oftop_lines_and_intervals,
                                               staff_left_x_offset, StaffConfig.STAFF_RIGHT_PADDING)
        current_staff = self.staff_builder.build_staff()
        current_staff.set_notes_boundaries() 
        current_staff.generate_bars()
        return current_staff
    
    def build_intervals(self, params: BuildStaffItemParams):
        intervals = []
        for i in range(params.no_of_items):
            interval_top_y = params.original_position.y + (i * (params.interval_thickness + params.line_thickness))
            interval_y_bottom = interval_top_y + params.interval_thickness - 1 # remove one cause start position is considered first pixel
            position_rect = Rect(Position(params.original_position.x, interval_top_y),
                                 Position(params.original_position.x + self.staff_width, interval_top_y),
                             Position(params.original_position.x + self.staff_width, interval_y_bottom),
                             Position(params.original_position.x, interval_y_bottom))          
            line_collateral_boundaries = CollateralBoundary(params.original_position.x + params.left_collateral_offset, params.original_position.x + 
                                                            self.staff_width - params.right_collateral_offset)
            staff_index = len(self.intervals) + 1 
            interval = Interval(position_rect, params.is_virtual, params.vertical_positioning, staff_index,
                                line_collateral_boundaries, self.staff.velocity, self.staff.tempo, self.staff)            
            intervals.append(interval)
        
        return intervals
    
    def build_lines(self, params:BuildStaffItemParams):
       
        for i in range(params.no_of_items):                 
            line_y = (i * (params.interval_thickness + params.line_thickness))
            start_position = Position(params.original_position.x, params.original_position.y + line_y)
            end_position = Position(params.original_position.x + self.staff_width, params.original_position.y + line_y) 
            line_collateral_boundaries = CollateralBoundary(start_position.x + params.left_collateral_offset,end_position.x - params.right_collateral_offset)
            staff_index = len(self.lines) + 1
            line = StaffLine(start_position, end_position, params.line_thickness, params.is_virtual, params.piano_key_details[i][0], params.piano_key_details[i],
                         params.vertical_positioning, staff_index, line_collateral_boundaries, self.staff.velocity, self.staff.tempo, self.staff)
            self.lines.append(line)
        
        return self
    
    def build_empty_staves(self, no_of_staves=1):
        staves = []
        if no_of_staves >= 0:
            for i in range(no_of_staves):
                staves.append(self.build_empty_staff())
            
        return staves

    

