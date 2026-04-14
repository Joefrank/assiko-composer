
from Builders.StaffBuilder import StaffBuilder
from Builders.StaffNoteBuilder import StaffNoteBuilder
from DataClasses.Config.ScreenConfig import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_ON, VERTICAL_POSITION_TOP, StaffConfig
from Model.Geometry.Position import Position
from Model.Score.GrandStaff import GrandStaff


class StaffBuilderDirector:
    
    def __init__(self):
        self.staff_builder = StaffBuilder()
        self.staff_note_builder = StaffNoteBuilder()
        self.interval_thickness = None
        self.line_thickness = None
        self.staff_spacing = None
        self.staff_no_lines = None
        self.staff_no_intervals = None
        self.staff_offset_margins_y = None

    @staticmethod
    def calculate_first_staff_position(window_width, staff_width_percentage, staff_original_y_offset):
        staff_with = window_width * staff_width_percentage / 100
        all_staves_x_offset = (window_width - staff_with) // 2
        return staff_with, Position(all_staves_x_offset, staff_original_y_offset)

    def build_staff(self, clef, time_signature, key_signature, staff_original_position, staff_vertical_padding,
                    staff_width, interval_thickness, line_thickness, staff_spacing, staff_no_lines, 
                    staff_no_intervals, tempo, velocity):
        self.interval_thickness = interval_thickness
        self.staff_offset_margins_y = staff_vertical_padding
        self.line_thickness = line_thickness
        self.staff_spacing = staff_spacing
        self.staff_no_lines = staff_no_lines
        self.staff_no_intervals = staff_no_intervals

        possible_no_oftop_lines_and_intervals = self.staff_offset_margins_y // (
                    self.interval_thickness + self.line_thickness)
        possible_staff_padding = possible_no_oftop_lines_and_intervals * (self.interval_thickness + self.line_thickness)
        # Initialize the staff
        self.staff_builder.init_staff(clef, time_signature, key_signature, staff_vertical_padding, staff_original_position, 
                                      staff_width, tempo, velocity)
        # Build music notes for staff and padding areas
        staff_note_items = self.staff_note_builder.build_staff_notes(clef, key_signature, possible_no_oftop_lines_and_intervals)

        # this gives the total number of lines and intervals we can fit in the staff_offset_margins_y
        # Build all lines and intervals above the staff        
        original_position = Position(staff_original_position.x, staff_original_position.y - possible_staff_padding)        
        top_notes = staff_note_items.top_of_staff_notes
        staff_notes = staff_note_items.staff_notes
        bottom_notes = staff_note_items.bottom_of_staff_notes
        staff_left_x_offset = self.staff_builder.calculate_left_collateral_offset(clef, key_signature)
        self.staff_builder.build_virtual_lines(self.interval_thickness, self.line_thickness, top_notes.line_notes, original_position, 
                                               VERTICAL_POSITION_TOP, possible_staff_padding, possible_no_oftop_lines_and_intervals, 
                                               staff_left_x_offset, StaffConfig.STAFF_RIGHT_PADDING)
        original_position = Position(original_position.x, original_position.y + self.line_thickness)
        
        self.staff_builder.build_virtual_intervals(self.interval_thickness, self.line_thickness, top_notes.interval_notes, 
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
    
    def build_grand_staff(self, window_width, StaffConfig, clef_tuple, time_signature, key_signature, tempo, velocity):
        # work out first staff position and width
        staff_with, staff_original_position = self.calculate_first_staff_position(window_width,
                                                                                      StaffConfig.STAFF_WIDTH_PERCENT,
                                                                                      StaffConfig.STAFF_ORIGINAL_Y_OFFSET)
        
        original_position = staff_original_position
        # build the top staff (treble).
        treble_staff = self.build_staff(clef_tuple[0], time_signature, key_signature,
                                                           staff_original_position,
                                                           StaffConfig.STAFF_ALLOWED_MARGIN, staff_with,
                                                           StaffConfig.STAFF_LINE_GAP,
                                                           StaffConfig.STAFF_LINE_THICKNESS,
                                                           StaffConfig.STAFF_SPACING,
                                                           StaffConfig.STAFF_NO_LINES,
                                                           StaffConfig.STAFF_NO_INTERVALS,
                                                           tempo, 
                                                           velocity)
        
        line_with_highest_y = max(treble_staff.virtual_lines, key=lambda line: line.start_position.y)
        staff_original_position = Position(staff_original_position.x, line_with_highest_y.start_position.y + StaffConfig.STAFF_SPACING)
        # build bottom staff (bass)
        bass_staff = self.build_staff(clef_tuple[1], time_signature, key_signature,
                                                           staff_original_position,
                                                           StaffConfig.STAFF_ALLOWED_MARGIN, staff_with,
                                                           StaffConfig.STAFF_LINE_GAP,
                                                           StaffConfig.STAFF_LINE_THICKNESS,
                                                           StaffConfig.STAFF_SPACING,
                                                           StaffConfig.STAFF_NO_LINES,
                                                           StaffConfig.STAFF_NO_INTERVALS,
                                                           tempo, 
                                                           velocity)
        
        bottom_virtual_line = max(bass_staff.virtual_lines, key=lambda line: line.end_position.y)
        grand_staff = GrandStaff([treble_staff, bass_staff], original_position, bottom_virtual_line.end_position)
        return grand_staff
    
  
