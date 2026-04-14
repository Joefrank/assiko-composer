

from DataClasses.Config.ScreenConfig import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_TOP
from DataClasses.Config.MusicConfig import supported_clef_settings
from Model.Geometry.Position import Position
from Model.Score import Interval, IntervalRect
from Model.Score.CollateralBoundary import CollateralBoundary
from Model.Score.Staff import Staff
from Model.Score.StaffLine import Line


class StaffBuilder:
    
    """
        clef: music clef of staff
        time_signature: time signature of staff
        key_signature: key signature of staff
        staff_vertical_padding: the distance at top and bottom of staff where we can add extra notes
        staff_top_left: the top left position of the staff
    """
    def __init__(self):        
        self.lines = []
        self.intervals = []
        self.staff = None
        self.staff_width = None
        self.staff_top_left = None
        self.staff_vertical_padding = None
  

    def get_current_staff(self):
        return self.staff    
   
    """ 
        nof_of_lines includes virtual lines
        interval_thickness: is the height of interval between two lines or line spacing
        line_thickness: tickness of each line on staff
        piano_key_details: dictionary containing raw_key: realpiano key e.g. ("E", "E4#")
        original_position: position where we start all lines in this call
        is_virtual: tells if interval is virtual or not
        vertical_positioning: tells if line is above, below (virtual) or on the staff
    """
    def build_lines(self, no_of_lines, interval_thickness, line_thickness, piano_key_details, original_position, is_virtual, 
                    vertical_positioning, left_collateral_offset, right_collateral_offset):
        #because we are starting to build lines from top to bottom and our key details are
        # from bottom to top, we need to reverse the array.  
        piano_key_details.reverse()  
        for i in range(no_of_lines):                 
            line_y = (i * (interval_thickness + line_thickness))
            start_position = Position(original_position.x, original_position.y + line_y)
            end_position = Position(original_position.x + self.staff_width, original_position.y + line_y) 
            line_collateral_boundaries = CollateralBoundary(start_position.x + left_collateral_offset,end_position.x - right_collateral_offset)
            staff_index = len(self.lines) + 1
            line = Line(start_position, end_position, line_thickness, is_virtual, piano_key_details[i][0], piano_key_details[i],
                         vertical_positioning, staff_index, line_collateral_boundaries, self.staff.velocity, self.staff.tempo, self.staff)
            self.lines.append(line)
        
        return self

    """
        Get the lowest staff line.
    """
    def get_staff_bottom_line(self):
        if len(self.lines) == 0:
            return
        return max(
            (line for line in self.lines if not line.is_virtual),
            key=lambda line: line.start_position.y,
            default=None
        )


    """
        Build intervals based on starting_position. 
        no_of_intervals includes virtual intervals
        interval_thickness: is the height of interval between two lines or line spacing. it's represented by the number of pixes the interval occupies.
            e.g. y_top: 140 - y_bottom: 149. the difference is 9 but as we count from 140, it is 10 pixels thickness 
        line_thickness: thickness of each line on staff
        piano_key_details: dictionary containing raw_key: real piano key e.g. ("E", "E4#")
        original_position: position where we start all intervals in this call
        is_virtual: tells if interval is virtual or not
        vertical_positioning: tells if interval is above, below (virtual) or on the staff
    """
    def build_intervals(self, no_of_intervals, interval_thickness, line_thickness, piano_key_details, original_position, is_virtual, vertical_positioning,
                        left_collateral_offset, right_collateral_offset):
        # because we are starting to build lines from top to bottom and our key details are
        # from bottom to top, we need to reverse the array.       
        piano_key_details.reverse()  
        for i in range(no_of_intervals):
            interval_top_y = original_position.y + (i * (interval_thickness + line_thickness))
            interval_y_bottom = interval_top_y + interval_thickness - 1 # remove one cause start position is considered first pixel
            position_rect = IntervalRect(Position(original_position.x, interval_top_y),
                                 Position(original_position.x + self.staff_width, interval_top_y),
                             Position(original_position.x + self.staff_width, interval_y_bottom),
                             Position(original_position.x, interval_y_bottom))          
            line_collateral_boundaries = CollateralBoundary(original_position.x + left_collateral_offset, original_position.x + 
                                                            self.staff_width - right_collateral_offset)
            staff_index = len(self.intervals) + 1 
            interval = Interval(position_rect, piano_key_details[i][0], piano_key_details[i], is_virtual, vertical_positioning, staff_index,
                                line_collateral_boundaries, self.staff.velocity, self.staff.tempo, self.staff)            
            self.intervals.append(interval)
        
        return self

    """
        A virtual interval is that holds extra notes above or below the staff.
        This function builds Virtual intervals based on starting_position on a specific staff.        
        interval_thickness: is the height of interval between two lines or line spacing. it's represented by the number of pixes the interval occupies.
            e.g. y_top: 140 - y_bottom: 149. the difference is 9 but as we count from 140, it is 10 pixels thickness 
        line_thickness: thickness of each line on staff
        piano_key_details: dictionary containing raw_key: real piano key e.g. ("E", "E4#")
        original_position: position where we start all interval in this call. It must be the top_left of staff or bottom_left of staff based on vertical_positioning
        is_virtual: tells if interval is virtual or not
        vertical_positioning: tells if interval is above, below (virtual) or on the staff
        staff_offset_margins_y: specifies how many pixes we can place virtual lines and intervals above/below staff. for 5 intervals, pass 5 * interval_tickness
    """
    def build_virtual_intervals(self, interval_thickness, line_thickness, piano_key_details, original_position, vertical_positioning, no_of_intervals,
                                 left_collateral_offset, right_collateral_offset):
        self.build_intervals(no_of_intervals, interval_thickness, line_thickness, piano_key_details, original_position,
                             True, vertical_positioning, left_collateral_offset, right_collateral_offset)
        
        return self

    """ 
       Builds virtual lines above/below staff based on provided offset.
       interval_thickness: is the height of interval between two lines or line spacing
       line_thickness: thickness of each line on staff
       piano_key_details: dictionary containing raw_key: realpiano key e.g. ("E", "E4#")
       original_position: position where we start all lines in this call
       vertical_positioning: tells if line is above, below (virtual) or on the staff
       staff_offset_margins_y: specifies how many pixes we can place virtual lines and intervals above/below staff. for 5 lines, pass 5 * interval_thickness
    """
    def build_virtual_lines(self, interval_thickness, line_thickness, piano_key_details, original_position, vertical_positioning,
                             staff_offset_margins_y, no_of_lines, left_collateral_offset, right_collateral_offset):
       
        self.build_lines(no_of_lines, interval_thickness, line_thickness, piano_key_details, original_position,
                         True, vertical_positioning, left_collateral_offset, right_collateral_offset)

        return self

    @staticmethod
    def work_out_offset_y(vertical_positioning, original_position, staff_offset_margins_y):
        if vertical_positioning == VERTICAL_POSITION_TOP:
            y_offset = original_position.y - staff_offset_margins_y
        elif vertical_positioning == VERTICAL_POSITION_BOTTOM:
            y_offset = original_position.y + staff_offset_margins_y
        else:
            y_offset = 0
            raise Exception(f"Invalid vertical_positioning for build_virtual_intervals(): {vertical_positioning}")

        # make sure offset is not negative as this will corrupt calculations. i.e. the offset that is not on the staff
        if y_offset < 0:
            y_offset *= -1

        return y_offset

    """
        We need to reorder our intervals based on their vertical/y positions. Virtual intervals are not displayed on staff.
    """
    def build_staff(self):    
        self.staff.lines = [line for line in self.lines if not line.is_virtual]
        self.staff.virtual_lines = [line for line in self.lines if line.is_virtual]
        self.staff.intervals = [interval for interval in self.intervals if not interval.is_virtual]   
        self.staff.virtual_intervals = [interval for interval in self.intervals if interval.is_virtual]
        self.set_position()
        return self.staff
    

    """
        Builds staff bounding coordinates.
        We calculate staff boundaries with real lines not virtual ones.
    """
    def set_position(self):
        normal_lines = [line for line in self.staff.lines if not line.is_virtual]
        self.staff.top_line = normal_lines[0]
        self.staff.bottom_line = normal_lines[-1]
        self.staff.position_rect = IntervalRect(self.staff.top_line.start_position,  self.staff.top_line.end_position,
                                        self.staff.bottom_line.end_position, self.staff.bottom_line.start_position)
        self.staff.top_position = self.staff.top_line.start_position
        self.staff.bottom_position = self.staff.bottom_line.start_position        

    """
        Works out left offset on staff/lines where we can start displaying notes and other musical signs.
        Ideally we leave 40 px for the clef and 20 px for each signature item.
    """
    def calculate_left_collateral_offset(self, clef, key_signature):
        signature_len = len(supported_clef_settings[clef]["signature_position_pattern"][key_signature])        
        clef_width = 40
        min_left_offset = 60 if signature_len < 3 else  (signature_len * 20) # minimum left offset if no clef or signature
        return clef_width + min_left_offset 


