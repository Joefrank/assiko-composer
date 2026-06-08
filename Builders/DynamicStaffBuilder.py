
"""
    Class is used to build staff progressively while user creates it and adds items to it.
"""
import pygame

from Builders.Params.BuildStaffItemParams import StaffItemBuildParams
from DataClasses.Config.ScreenConfig import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_TOP, StaffConfig
from Model.Geometry.Position import Position
from Model.Score.CollateralBoundary import CollateralBoundary
from Model.Score.Interval import Interval
from Model.Score.Rect import Rect
from Model.Score.Staff import Staff
from Model.Score.StaffLine import StaffLine
from Renderers.StaffRenderer import StaffRenderer


class DynamicStaffBuilder:

    def __init__(self, app_state):        
        self.all_staves = []
        # work out first staff position and width
        #self.staff_with, self.staff_original_position = self.calculate_first_staff_position(container,
                                                                                     # StaffConfig.STAFF_WIDTH_PERCENT,
                                                                                     # StaffConfig.STAFF_ORIGINAL_Y_OFFSET)
        self.app_state = app_state
        self.next_staff_position = None
        self.staff_height = self.calculate_staff_height()
        self.staff_renderer = StaffRenderer(app_state)


    def calculate_staff_height(self):
        return (StaffConfig.STAFF_NO_LINES * StaffConfig.STAFF_LINE_THICKNESS) + (StaffConfig.STAFF_NO_INTERVALS * StaffConfig.STAFF_LINE_GAP)
  

    """
    staff_virtual_position is the position where the first virtual line will be placed. 
    This is calculated based on the original position of the staff and the exact padding we have for virtual items. This is because we want to make sure that we have enough space for all virtual items above the staff without overlapping with the staff lines and intervals.
    """
    def create_staff_build_params(self, position, staff):  
           
        staff_original_position = position
        staff_width = staff.rect.width
        # set original position for top virtual items.
        line_and_interval_tickness = (StaffConfig.STAFF_LINE_GAP + StaffConfig.STAFF_LINE_THICKNESS)        
        no_virtual_items_per_section = StaffConfig.STAFF_ALLOWED_MARGIN // line_and_interval_tickness            
        staff_exact_padding = no_virtual_items_per_section * line_and_interval_tickness
        staff_virtual_position = Position(staff_original_position.x, staff_original_position.y - staff_exact_padding) 

        # Virtual items above the staff, we have same no of virtual lines as intervals.
        top_virtual_items_param = StaffItemBuildParams(
            no_of_items=no_virtual_items_per_section,
            staff_width=staff_width,
            original_position=staff_virtual_position,
            parent_staff=staff,
            is_virtual=True,
            vertical_positioning=VERTICAL_POSITION_TOP
        )    

        # reset original position for staff contained items.
        staff_lines_params = StaffItemBuildParams(
            no_of_items=StaffConfig.STAFF_NO_LINES,
            staff_width=staff_width,
            original_position=staff_original_position,
            parent_staff=staff,
        )

        staff_intervals_params = StaffItemBuildParams(
            no_of_items=StaffConfig.STAFF_NO_INTERVALS,
            staff_width=staff_width,
            original_position=Position(staff_original_position.x, 
                                       staff_original_position.y + StaffConfig.STAFF_LINE_THICKNESS),            
            parent_staff=staff
        )

        bottom_virtual_items_param = StaffItemBuildParams(
            no_of_items=no_virtual_items_per_section,
            staff_width=staff_width,
            original_position=staff_original_position,            
            parent_staff=staff,
            is_virtual=True,
            vertical_positioning=VERTICAL_POSITION_BOTTOM
        )    

        return top_virtual_items_param, staff_lines_params, staff_intervals_params, bottom_virtual_items_param
    
     
    def build_empty_staff(self, top_left_position, staff_width):            
        # Prepare parameters for building staff components (lines and intervals) and virtual components (lines and intervals above and below the staff)
        staff = Staff(pygame.Rect(top_left_position[0], top_left_position[1], staff_width, self.staff_height), len(self.all_staves) + 1, self.staff_renderer) 
        top_virtual_items_param, staff_lines_params, staff_intervals_params, bottom_virtual_items_param =\
        self.create_staff_build_params(Position(top_left_position[0], top_left_position[1]), staff)
        
        # build and set virtual lines for the staff.
        staff.virtual_lines += self.build_lines(top_virtual_items_param)
        # we need to update the original position for the intervals because they start after the first line thickness
        next_y_offset = top_virtual_items_param.original_position.y + StaffConfig.STAFF_LINE_THICKNESS
        top_virtual_items_param.original_position.moveVerticallyTo(next_y_offset)
        # Build and set virtual intervals for the staff.
        staff.virtual_intervals += self.build_intervals(top_virtual_items_param)

        # Build and set lines and intervals for the staff.
        staff.lines += self.build_lines(staff_lines_params)
        staff.intervals += self.build_intervals(staff_intervals_params)

         # Adjust original position for bottom virtual items because they start after the last line thickness
        staff_bottom_line = staff.get_staff_bottom_line()        
        bottom_virtual_items_param.original_position.moveVerticallyTo(staff_bottom_line.start_position.y +\
                                                                       StaffConfig.STAFF_LINE_THICKNESS) 
        
        # Now, build the bottom virtual intervals.
        staff.virtual_intervals += self.build_intervals(bottom_virtual_items_param)
        # Adjust original position for bottom virtual lines because they start after the last interval thickness
        bottom_virtual_items_param.original_position.moveVerticallyTo(staff_bottom_line.start_position.y +\
                                                 StaffConfig.STAFF_LINE_GAP + StaffConfig.STAFF_LINE_THICKNESS)
        # Finally, build the bottom virtual lines.
        staff.virtual_lines += self.build_lines(bottom_virtual_items_param)     
       
        staff.set_positions()
        self.all_staves.append(staff)
        return staff
       
    def set_next_staff_position(self):
        if not self.all_staves:
            self.next_staff_position = self.staff_original_position
        else:
            last_staff = self.all_staves[-1]
            last_staff_bottom_line = last_staff.get_bottom_virtual_line()
            next_y_offset = last_staff_bottom_line.start_position.y + StaffConfig.STAFF_SPACING
            self.next_staff_position = Position(self.staff_original_position.x, next_y_offset)


    def build_intervals(self, params: StaffItemBuildParams):
        intervals = []
        for i in range(params.no_of_items):
            interval_top_y = params.original_position.y + (i * (params.interval_thickness + params.line_thickness))
            interval_y_bottom = interval_top_y + params.interval_thickness - 1 # remove one cause start position is considered first pixel
            position_rect = Rect(Position(params.original_position.x, interval_top_y),
                                 Position(params.original_position.x + params.staff_width, interval_top_y),
                             Position(params.original_position.x + params.staff_width, interval_y_bottom),
                             Position(params.original_position.x, interval_y_bottom))          
            line_collateral_boundaries = CollateralBoundary(params.original_position.x + params.left_collateral_offset, params.original_position.x + 
                                                            params.staff_width - params.right_collateral_offset)
            staff_index = i + 1 

    
            interval = Interval(position_rect, params.key, None, params.is_virtual, params.vertical_positioning, staff_index,
                                line_collateral_boundaries, params.velocity, params.tempo, params.parent_staff)            
            intervals.append(interval)
        
        return intervals
    
    def build_lines(self, params:StaffItemBuildParams):
        lines = []
        for i in range(params.no_of_items):                 
            line_y = (i * (params.interval_thickness + params.line_thickness))
            start_position = Position(params.original_position.x, params.original_position.y + line_y)
            end_position = Position(params.original_position.x + params.staff_width, params.original_position.y + line_y) 
            line_collateral_boundaries = CollateralBoundary(start_position.x + params.left_collateral_offset,end_position.x - params.right_collateral_offset)
            staff_index = i + 1
            line = StaffLine(start_position, end_position, params.line_thickness, staff_index, None, None,
                         params.is_virtual, params.vertical_positioning, line_collateral_boundaries, 
                         None, None, params.parent_staff)
            lines.append(line)
        
        return lines
    
    def build_empty_staves(self, top_left_position, staff_width, no_of_staves=1):
        staves = []
        if no_of_staves >= 0:
            for i in range(no_of_staves):
                staves.append(self.build_empty_staff(top_left_position, staff_width))
            
        return staves

    """Because staff is inside a scrollable container, the container for score is at position (0,0) and we work out all 
    staff positions based on this. So, we need to calculate the first staff position based on the container position and then calculate the next staff positions based on the first staff position and the spacing we want between staves."""
    @staticmethod
    def calculate_first_staff_position(container, staff_width_percentage, staff_original_y_offset):
        container_width = container.rect.width
        staff_with = container_width * staff_width_percentage / 100
        all_staves_x_offset = int((container_width - staff_with) // 2) 
        return staff_with, Position(all_staves_x_offset, staff_original_y_offset)
    
    
    