import pygame
from datetime import datetime
from DataClasses.Config import ScreenConfig
from DataClasses.Config.ScreenConfig import Color, StaffConfig
from DataClasses.Config.MusicConfig import supported_clef_settings, \
    supported_time_signatures, supported_modulations
from Helpers.ScreeHelper import ScreenHelper
from Model.Geometry.Position import Position
from Model.Score.Helpers import StaffUtils
from Model.Score.Interval import Interval
from Model.Score.Note import Note
from Model.Score.StaffLine import StaffLine
from Renderers.BaseRenderer import BaseRenderer


class StaffRenderer(BaseRenderer):

   
    def __init__(self, state):
        super().__init__(state) 
        self.start_time = datetime.now().time()        
        self.MODULATION_SPACING = 6
        self.STAFF_ITEM_LINE = 0
        self.STAFF_ITEM_INTERVAL = 1
        self.music_score = None
        self.piano_notes = None 
        self.sound_player = state.sound_player
      
    def render_grand_staff(self, grand_staff, screen):
        previous_staff = None
        for staff in grand_staff.staves:
            self.render_staff(staff, screen)
            if previous_staff is not None:
                self.bind_staves(previous_staff, staff)
            previous_staff = staff

    def bind_staves(self, top_staff, bottom_staff):
        self.draw_line_from_point(top_staff.top_position, bottom_staff.top_position, thickness=2)

    """ Displays a single staff on our music score."""
    def render_staff(self, staff, screen): 
        self.draw_staff_boundaries(staff, screen)   
        # For a blank staff, there will be no clef.     
        clef_position = self.draw_staff_clef(staff, screen)
        key_signature_position = Position(clef_position.x + 20, clef_position.y)
        last_offset_x = self.draw_key_signature(staff, key_signature_position, screen)
        last_offset_x += 30
        _, _, end_offset = self.draw_time_signature(screen, staff.time_signature, Position(last_offset_x, staff.top_position.y))  
        # Collaterals are every music symbols to be drawn on or around the staff. 
        end_offset += 30            
        self.render_staff_items(staff)

    """
        Renders all items: lines, intervals, notes and other musical items. 
    """
    def render_staff_items(self, staff):
        self.render_staff_intervals(staff)
        self.render_staff_lines(staff)
        self.render_staff_bars(staff)

    """ We don't normally display intervals but lines show gaps which are intervals. 
        But we do display the contained elements (musical items) on screen."""  
    def render_staff_intervals(self, staff):
        for interval in staff.intervals:
            self.draw_staff_item_collaterals(interval, staff)
           
        for interval in staff.virtual_intervals:
            self.draw_staff_item_collaterals(interval, staff, nearest_staff=staff)

    """ Display all staff lines (virtual and non-virtual) and contained elements on screen."""
    def render_staff_lines(self, staff):
        for line in staff.lines:
            self.draw_line(line)            
            self.draw_staff_item_collaterals(line, staff)
           
        for line in staff.virtual_lines:
            self.draw_staff_item_collaterals(line, staff, nearest_staff=staff) 

    """ Displays staff bars """
    def render_staff_bars(self, staff):
        for bar in staff.bars:
            self.draw_line(bar.line)   

    """
        Draws any items in ApplicationState that collide with the line
    """
    def draw_staff_item_collaterals(self, staff_item, staff, nearest_staff=None):
        mouse_over_position = self.state.mouse_hover.get_current_position()
        # if staff item has notes, we want to display them.
        if len(staff_item.notes) > 0:
            for note in staff_item.notes:
                note_color = Color.RED if self.state.last_note_added == note else \
                    (Color.BLACK if note.color is None else note.color)
                related_chord_notes = staff.get_notes(note.position.x)  # to ensure we get notes with x offset if any
                if len(related_chord_notes) > 1:
                    INVERTED_BY_DEFAULT = staff.is_stem_inverted_by_default()
                    self.render_chord(related_chord_notes, inverted=INVERTED_BY_DEFAULT)
                else:
                    self.render_note(note, True, note_color, Color.GREY)
                    
                if staff_item.is_virtual: # show virtual lines
                    self.render_virtual_lines_to_staff(nearest_staff, staff_item, note.position)

        if mouse_over_position is None:
            return

        # if there is a hovering item, display mouse tracker
        if staff_item.mouse_hovering_around(mouse_over_position, StaffConfig.STAFF_ITEM_THRESHOLD):                        
            self.render_mouse_tracker(mouse_over_position, staff_item.key_id)
            mouse_position = Position(mouse_over_position.x, mouse_over_position.y)           

            if staff_item.is_virtual and nearest_staff is not None:
                self.render_virtual_lines_to_staff(nearest_staff, staff_item, mouse_position)

            self.state.mouse_hover.reset_current_position()

    """
        Draws virtual lines from position clicked above or below staff all the way to staff.
        staff: is nearest staff
        staff_item: item (line/interval) holding the mouse click position
        mouse_position: actual click position.
    """
    def render_virtual_lines_to_staff(self, staff, staff_item, mouse_position):
        moving_factor = 0
        # check if position is top or bottom of staff
        if mouse_position.is_above_position(staff.top_position):
            start_position = mouse_position                   
            moving_factor = 1 # top to bottom direction
        elif mouse_position.is_below_position(staff.bottom_position):
            start_position = mouse_position
            moving_factor = -1 # bottom to top direction

        if isinstance(staff_item, StaffLine):
            self.draw_virtual_lines(moving_factor, start_position, staff, include_colliding_line=True)
        elif isinstance(staff_item, Interval):
            self.draw_virtual_lines(moving_factor, start_position, staff)

    """
        Draws all virtual lines from position on top or bottom of staff all the way to it.
        moving_factor: direction in which we draw virtual lines. moving down (1) or up (-1), 
        mouse_position: last recorded position of the mouse (in state), 
        nearest_staff: closest staff to the mouse_position, 
        include_colliding_line: tells if we draw the line on mouse_position (True for lines and False for intervals)
    """
    def draw_virtual_lines(self, moving_factor, mouse_position, nearest_staff, include_colliding_line = False):
        for line in nearest_staff.virtual_lines:# we only draw lines. intervals are visible between lines
            virtual_line_position = Position(mouse_position.x, line.start_position.y)
            # if mouse position is on top of staff
            if ((moving_factor == 1 and line.is_above_position(nearest_staff.top_position) 
                and line.is_below_position(mouse_position))  
                or (include_colliding_line and line.contains_position(mouse_position))): 
                self.draw_virtual_line(self.screen, virtual_line_position, color=Color.RED, 
                                       specified_line_width=StaffConfig.VIRTUAL_LINE_WIDTH)
            # if the mouse_position is below the staff
            elif ((moving_factor == -1 and line.is_below_position(nearest_staff.bottom_position)
                   and line.is_above_position(mouse_position)) 
                   or (include_colliding_line and line.contains_position(mouse_position))):
                self.draw_virtual_line(self.screen, virtual_line_position, color=Color.BLUE, 
                                       specified_line_width=StaffConfig.VIRTUAL_LINE_WIDTH)           

    def render_note_at_position(self, mouse_position, staff_item, tempo, velocity):
         # Adjust position to be position of staff_item (line/interval)
         if isinstance(staff_item, StaffLine):
             note_position = Position(mouse_position.x, staff_item.start_position.y)
         elif isinstance(staff_item, Interval):
             rect = staff_item.position_rect
             y_offset =  ((rect.bottom_left.y - rect.top_left.y) // 2)
             note_position = Position(mouse_position.x, rect.top_left.y + y_offset)
            
         # change note duration to key pressed        
         note_duration = self.get_registered_note_duration()
         # get the note order
         note_order = staff_item.get_next_note_index() 
         note_extended = False     
         new_note = Note(staff_item, note_duration, note_position, note_order, note_extended, staff_item.key,
                         staff_item.key_id, tempo, velocity)
        
         new_note.set_parent(staff_item)
         staff_item.add_note(new_note)  
         return new_note    
    
    def draw_staff_boundaries(self, staff, screen=None):
        if screen is None:
            screen = self.screen
        self.draw_line_from_point(staff.position_rect.top_left, staff.position_rect.bottom_left, thickness=2, screen=screen)
        self.draw_line_from_point(staff.position_rect.top_right, staff.position_rect.bottom_right, thickness=2, screen=screen)

    """
        Draws a virtual line at the top or bottom of the staff
        line: the line matching/holding our point/position
        position: the center of our virtual line (mouse position) 
    """ 
    def draw_virtual_line(self, screen, position, color=(0, 0, 0), thickness=1, specified_line_width=20):            
        start_x = position.x - (specified_line_width // 2)
        end_x = start_x + specified_line_width
        pygame.draw.line(screen, color, (start_x, position.y),
                         (end_x,  position.y), thickness) 
  
    """
        Draws the clef on the staff.
    """
    def draw_staff_clef(self, staff, font_color=(0, 0, 0), screen=None):
        if staff.clef is None:
            return staff.top_position
        if screen is None:
            screen = self.screen
        clef_settings = supported_clef_settings[staff.clef]
        clef_size = clef_settings["size"]
        clef_font_size =ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, clef_size)) 
        clef = clef_font_size.render(clef_settings["font_code"], True, font_color)
        # Get clef rect to position it
        clef_rect = clef.get_rect()
        clef_position = StaffUtils.resolve_position_with_margins(staff.position_rect.top_left, clef_settings["margins"])
        clef_rect.center = (clef_position.x, clef_position.y)
        screen.blit(clef, clef_rect)
        return clef_position
    
    """
        Draws the time signature specified for the staff
    """
    def draw_time_signature(self, screen, time_signature, position, font_color=(0, 0, 0)):
        if time_signature is None:
            return (0,0), (0,0), position.x
        
        time_signature_fonts = supported_time_signatures[time_signature]["symbol"]
        item_size = supported_time_signatures[time_signature]["size"]
        item_margins = supported_time_signatures[time_signature]["margins"]
        item_font = ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, item_size))       
        time_numerator = item_font.render(time_signature_fonts[0], True, font_color)
        time_denominator = item_font.render(time_signature_fonts[1], True, font_color)
        # Get clef rect to position it
        numerator_rect = time_numerator.get_rect()
        denominator_rect = time_denominator.get_rect()
        numerator_rect.center = (position.x + item_margins[0], position.y + item_margins[1])
        denominator_rect.center = (position.x + item_margins[2], position.y + item_margins[3]  + (item_size // 2))
        screen.blit(time_numerator, numerator_rect)
        screen.blit(time_denominator, denominator_rect)
        next_x_offset = position.x + item_size
        return numerator_rect.center, denominator_rect.center, next_x_offset
    
    """
        Draws the key signature of the staff
    """
    def draw_key_signature(self, staff, reference_position, screen=None):
        if screen is None:
            screen = self.screen

        if staff.key_signature is None:# normally return an error message ***
            return reference_position.x
        
        clef_settings = supported_clef_settings[staff.clef]
        signature_patterns =clef_settings["signature_position_pattern"]
        signature_details = signature_patterns[staff.key_signature]
        modulation_name, modulation_details = StaffUtils.find_key_signature_modulation(staff.key_signature, supported_modulations)
        modulation_font_code = modulation_details["font_code"]
        modulation_font_size =  modulation_details["font_size"]
        modulation_item_index = 1
        last_modulation_x_offset = 0 # needed to position next item (time signature)
        
        for pattern in signature_details:
            signature_item_positioning = next(iter(pattern.values()))
            staff_item_type = signature_item_positioning[0] # line/interval
            staff_item_position = None

            if staff_item_type == self.STAFF_ITEM_LINE: # line
                staff_item_position = StaffUtils.get_signature_item_coordinates_for_line(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
                                                                modulation_font_size, staff.lines, signature_item_positioning[1], 
                                                                self.MODULATION_SPACING, reference_position.x)
            elif staff_item_type == self.STAFF_ITEM_INTERVAL: # interval
                staff_item_position = StaffUtils.get_signature_item_coordinates_for_interval(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
                                                                                   modulation_font_size, staff.lines,
                                                                                   staff.intervals, signature_item_positioning[1], self.MODULATION_SPACING, reference_position.x)

            signature_position = (staff_item_position.x, staff_item_position.y)
            self.draw_modulation(screen, modulation_font_code, StaffConfig.STAFF_MODULATION_FONT_SIZE,
                                 signature_position)
            modulation_item_index += 1
            last_modulation_x_offset = staff_item_position.x

        return 90 if len(signature_details) < 1 else last_modulation_x_offset
    
    """
        Displays modulation at specific position # or b on line or interval
    """
    def draw_modulation(self, screen, modulation_font_code, modulation_font_size, position, modulation_color=(0, 0, 0)):
        modulation_font = ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, modulation_font_size))
        modulation = modulation_font.render(modulation_font_code, True, modulation_color)
        # Get clef rect to position it
        modulation_rect = modulation.get_rect()
        modulation_rect.center = position
        screen.blit(modulation, modulation_rect)