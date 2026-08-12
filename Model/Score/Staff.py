from DataClasses.ButtonConfigData import ActionButtonConfig, ActionButtonGroupConfig, ActionButtonPosition, ActionIdentifiers
from DataClasses.Config.ScreenConfig import StaffConfig
from DataClasses.Config.MusicConfig import supported_time_signatures,TREBLE_CLEF, BARITON_CLEF
from DataClasses.ControlData import ControlType
from Model.Dialogs.DialogModifyStruct import DialogModifyStruct
from Model.Geometry.Position import Position
from Model.Geometry.Line import Line
from Model.Score.Clef import Clef
from Model.Score.Note import Note
from Model.Score.ScoreControl import ScoreControl
from Model.Score.StaffBar import StaffBar
from Renderers.StaffRenderer import StaffRenderer

class Staff(ScoreControl):   
    
    CONFIRM_DELETION_DIALOG_KEY = "CONFIRM_STAFF_DELETION_DIALOG"

    def __init__(self, rect, staff_number, staff_renderer, parent_page, clef=None, time_signature=None, 
                 key_signature=None, tempo:int=None, velocity:int=None):
        super().__init__(rect, ControlType.STAFF, f"Staff {staff_number}", parent=None)
       
         # position attributes
        self.position_rect = rect
        self.top_position = None #postion of top line of staff
        self.bottom_position = None #position of bottom line of staff
        self.bottom_line = None # not necessary a line on the staff but how far below you can go with the ledger
        self.top_line = None # not necessary a line on the staff but how far above you can go with the ledger        
        # note boundaries attributes
        self.notes_left_offset = 0 # this is the left boundary for notes on this staff.
        self.notes_right_offset = 0 # this is the right boundary for notes on this staff.
        self.notes_top_offset = 0 # top boundary for notes belonging to this staff
        self.notes_bottom_offset = 0 # bottom boundary for notes belonging to this staff
        
        # Staff children components
        self.lines = [] 
        self.intervals = []
        self.virtual_lines = [] # any lines above or below staff
        self.virtual_intervals = [] #any interval above or below staff
        self.modulations = []
        self.bars = []
        self.clef = clef
        self.time_signature = time_signature
        self.key_signature = key_signature
        self.step_notes_rests_lyrics = []  # these are chords played in steps. It's a list of StaffStep
        self.dynamics = [] # use StaffDynamic as a list
        self.lyrics_lines = []  
        self.action_buttons = []

        self.velocity:int = velocity
        self.tempo:int = tempo  
       
        self.staff_renderer:StaffRenderer = staff_renderer
        self.staff_number = staff_number   
        self.parent_page = parent_page
        self.action_icon_rects = {}        
      
    @property
    def top_left_position(self):
        return self.rect.topleft
    
    @property
    def bottom_right_position(self):
        return self.rect.bottomright
    
    @property
    def bottom_left_position(self):
        return self.rect.bottomleft
    
    @property
    def top_right_position(self):
        return self.rect.topright
    
    def set_notes_boundaries(self):
        self.notes_left_offset = self.top_line.line_collateral_boundaries.left_boundary
        self.notes_right_offset = self.top_line.line_collateral_boundaries.right_boundary
        self.notes_top_offset = self.top_line.start_position.y
        self.notes_bottom_offset = self.bottom_line.start_position.y

    def get_width(self):
        return self.rect.width
    
    def get_height(self):
        return self.bottom_position.y - self.top_position.y 

    """ The nearest note to a position is the note that comes closer in distance to a specific position on the staff. """
    def find_nearest_note(self, position) -> Note:
        # Collect all note groups from both lines and intervals
        note_groups = [line.get_notes() for line in self.lines] + \
                    [interval.get_notes() for interval in self.intervals] + \
                    [line.get_notes() for line in self.virtual_lines] + \
                    [interval.get_notes() for interval in self.virtual_intervals]

        _, nearest_note = self._find_nearest_in_groups(note_groups, position)
        return nearest_note

    """ The nearest staff item to a position is the staff item (line or interval) that contains a note closest to the position. """
    def find_nearest_item_to_position(self, position):
       # Collect all staff items from both lines and intervals
        staff_items = [line for line in self.lines] + \
                    [interval for interval in self.intervals] + \
                    [line for line in self.virtual_lines] + \
                    [interval for interval in self.virtual_intervals]
        
        for staff_item in staff_items:
            if staff_item.mouse_hovering_around(position, StaffConfig.STAFF_ITEM_THRESHOLD):
                return staff_item
        return None
    
    def _find_nearest_in_groups(self, note_groups, position):
        smallest_distance = -1
        nearest_note = None

        for notes in note_groups:
            distance, note = self.find_nearest_note_from_notes(notes, position)
            if distance != -1 and (smallest_distance == -1 or distance < smallest_distance):
                smallest_distance = distance
                nearest_note = note

        if nearest_note is None or nearest_note.is_near_position(position) == False:            
            return -1, None
        else:
            return smallest_distance, nearest_note


    def find_nearest_note_from_notes(self, notes, position):
        if not notes:
            return -1, None

        smallest_distance = -1
        nearest_note = None

        for note in notes:
            distance = note.get_distance_to(position)

            if distance == 0:
                return 0, note

            if smallest_distance == -1 or distance < smallest_distance:
                smallest_distance = distance
                nearest_note = note

        return smallest_distance, nearest_note
    
    def get_top_left(self):
        return self.top_position

    def get_bottom_left(self):
        return self.bottom_position
    
    def get_notes_offsets(self):
        return (self.notes_left_offset, self.notes_right_offset)
    
    def get_initial_navigator_line(self):
        navigator_top_left = Position(self.notes_left_offset, self.top_position.y)
        navigator_bottom_left = Position(self.notes_left_offset, self.bottom_position.y)
        return (navigator_top_left, navigator_bottom_left)
    
    def get_notes(self, x_offset=None) -> list[Note]:
        notes = []
        for line in self.lines:
            notes.extend(line.get_notes(x_offset))
        for line in self.virtual_lines:
            notes.extend(line.get_notes(x_offset))
        for interval in self.intervals:
            notes.extend(interval.get_notes(x_offset))
        for interval in self.virtual_intervals:
            notes.extend(interval.get_notes(x_offset))
        return notes
    
    def get_chords(self):
        from Model.Score.Chord import Chord
        chords = []
        all_staff_notes = self.get_notes()
        # group all notes by x position into chords
        for x in range(int(self.notes_left_offset), int(self.notes_right_offset) + 1):
            notes_at_x = [note for note in all_staff_notes if note.position.x == x]
            if notes_at_x:
                note_list = []                
                for note in notes_at_x:
                    note_list.append(note)
                
                if len(note_list) > 0:
                    chord = Chord("", x)   
                    chord.set_notes(note_list)              
                    chords.append(chord)

        return chords  
    
    """ This generates bars for the current staff based on time signature.
        The width of bars also should be based on no of items (notes or rests) in each bar.
    """
    def generate_bars(self):
        (numerator, denominator) = supported_time_signatures[self.time_signature]["fraction"]
        notes_space = self.notes_right_offset - self.notes_left_offset
        # if there are no notes, just add bars evenly. we will have a sync function to re-arrange based on notes.
        factor = 2 if denominator != 4 else 1 # we want bigger bars and less if denominator is not 4
        bar_width = (numerator * StaffConfig.STAFF_NOTE_SPACE * factor)
        no_of_bars = int(notes_space // bar_width)
        # create and register all bars
        previous_bar = None       
        for bar_index in range(1, no_of_bars + 1):
            x_offset = self.notes_left_offset + (bar_index * bar_width)
            bar_line = Line(Position(x_offset, self.notes_top_offset), 
                                    Position(x_offset, self.notes_bottom_offset), StaffConfig.STAFF_BAR_THICKNESS)
            bar = StaffBar(previous_bar, None, bar_line)
            self.bars.append(bar)
            if previous_bar is not None:
                previous_bar.set_next(bar)  

    def is_stem_inverted_by_default(self):
        return self.clef in [TREBLE_CLEF, BARITON_CLEF]
    
    def get_staff_bottom_line(self):
        if len(self.lines) == 0:
            return
        return max(
            (line for line in self.lines if not line.is_virtual),
            key=lambda line: line.start_position.y,
            default=None
        )
    
    def get_bottom_virtual_line(self):
        if len(self.virtual_lines) == 0:
            return
        return max(
            (line for line in self.virtual_lines if line.is_virtual),
            key=lambda line: line.start_position.y,
            default=None
        )
    
    # No longer needed since we have get_bottom_virtual_line and get_staff_bottom_line
    # def set_positions(self):       
    #     self.top_line = self.lines[0]
    #     self.bottom_line = self.lines[-1]
    #     self.position_rect = IntervalRect(self.top_line.start_position,  self.top_line.end_position,
    #                                     self.bottom_line.end_position, self.bottom_line.start_position)
    #     self.top_position = self.rect.start_position
    #     self.bottom_position = self.rect.bottom_left    
  
 
    def draw(self, scrollable_screen=None):
        if scrollable_screen is not None:
            self.staff_renderer.set_screen(scrollable_screen)
        
        # Get scroll offset from parent page
        parent_page = self.parent_page
        previous_vertical_offset = self.staff_renderer.vertical_offset
 
        # Apply the parent page's scroll offset (which comes from scrollview:parent_container)
        if parent_page and hasattr(parent_page, 'parent') and hasattr(parent_page.parent, 'scroll_y'):
            self.staff_renderer.vertical_offset = parent_page.parent.scroll_y
        else:
            self.staff_renderer.vertical_offset = 0

        # Let a special renderer display the staff because it's complex
        try:
            self.staff_renderer.render_staff(self)
        finally:
            self.staff_renderer.vertical_offset = previous_vertical_offset
    
    def map_coordinates_in_viewport(self, coordinates:tuple) -> tuple:
        return self.parent_page.map_coordinates_in_viewport(coordinates)
    
    """
        Staff override move because it needs to move all its children.
        Staff offset_x should not change otherwise the alignment get messed up on page.
        offset_y: is the difference between original position and target one.
    """
    def move(self, _, offset_y):
        actual_offset_y = offset_y

        parent_page = self.get_parent()
        parent_container = getattr(parent_page, "parent_container", None)
        pages = getattr(parent_container, "children", None)

        if pages and len(pages) > 0 and hasattr(self.rect, "height"):
            first_page_top = pages[0].rect.top
            last_page_bottom = pages[-1].rect.bottom

            min_y = first_page_top
            max_y = last_page_bottom - self.rect.height

            if max_y < min_y:
                max_y = min_y

            target_y = self.rect.y + offset_y
            clamped_y = max(min_y, min(max_y, target_y))
            actual_offset_y = clamped_y - self.rect.y
       
        super().move_y(actual_offset_y)        
        for child in self.get_children():
            child.move_y(actual_offset_y)

    def duplicate_staff_below(self, caller):
        self.add_new_staff_below(self)
       
    def add_new_staff_below(self, staff):
        staff_builder = self.main_window.staff_builder
        # get top left position for new staff based on the bottom of the current staff and spacing
        new_staff_top_left = (
            self.rect.x,
            self.rect.bottom + StaffConfig.STAFF_SPACING
        )

        # build the staff and add it to the parent page
        staff_actions = [ActionButtonGroupConfig(ActionButtonPosition.RIGHT, 
                                                 [ActionIdentifiers.ADD_STAFF_ACTION, 
                                                  ActionIdentifiers.DELETE_STAFF_ACTION,
                                                  ActionIdentifiers.CREATE_GRAND_STAFF_ACTION,
                                                  ActionIdentifiers.EXTEND_GRAND_STAFF_ACTION])]
        new_staff = staff_builder.build_empty_staff(
            new_staff_top_left,
            StaffConfig.STAFF_WIDTH_PERCENT,
            self.parent_page,
            staff_actions
        )
        
        self.parent_page.add_child(new_staff)  # Add the new staff to the parent page
        self.shift_objects_below_staff(staff)

        return new_staff

        
    """ Do this in parent page  because it has better control of all children objecst."""
    def shift_objects_below_staff(self, staff):
        # find all staves below the current staff
        all_staves_below = [s for s in self.parent_page.children if isinstance(s, Staff) and s.rect.y > staff.rect.y]
        
        if all_staves_below:
            # push all staves below down by the height of the new staff plus spacing
            parent_container = getattr(self.parent_page, "parent_container", None)
            for s in all_staves_below:
                # we need to check that after moving down staff sits within a page. If not, we need to create a new page and move the staff to that page.
                last_staff_bottom = s.rect.bottom + StaffConfig.STAFF_SPACING               
                if parent_container and hasattr(parent_container, "rect"):
                    container_bottom = parent_container.rect.bottom
                    if last_staff_bottom > container_bottom:
                        # Create a new page and move the staff to that page
                        new_page = self.main_window.page_builder.build_new_page(parent_container)
                        new_page.add_child(s)
                        s.set_parent(new_page)
                        s.set_position(s.rect.x, new_page.rect.y + StaffConfig.STAFF_SPACING)
                    else:
                        s.move(0, last_staff_bottom - s.rect.y)        

    def confirm_delete(self, caller):        
        dialog_config = DialogModifyStruct(
            main_window=self.main_window,
            dialog_title=self.translate("CONFIRM_DELETE_STAFF_TITLE"),
            dialog_message=self.translate("CONFIRM_DELETE_STAFF_MESSAGE"),
            target=caller.parent            
        )
        callbacks = [self.delete_staff, self.cancel_dialog]         
        dialog = self.build_delete_confirm_dialog(caller, dialog_config, callbacks) 
        dialog.show()
       
        ## when you open dialog, you need to disable all actions and events apart from the dialog.
      
    def delete_staff(self, target):         
         target.delete()
         if target.last_opened_dialog:
             target.last_opened_dialog.close()
             target.last_opened_dialog = None  

    def change_action_button_target_control(self, new_target):
        for button in self.action_buttons:
            button.change_target_control(new_target)

    """Converts current staff to a grand staff by creating a new staff below it and combining them into a grand staff."""
    def convert_to_grand_staff(self, caller):
        original_staff = caller.parent
        
        # Work out position of new staff
        new_staff_top_left = (
            original_staff.rect.x,
            original_staff.rect.bottomleft[1] + StaffConfig.STAFF_SPACING
        )

        # Create a new staff below the current staff
        new_staff = self.main_window.staff_builder.build_empty_staff(
            new_staff_top_left,StaffConfig.STAFF_WIDTH_PERCENT, parent_page=self.parent_page
        )

        # create a grand staff by combining the current staff and the new staff. 
        grand_staff = self.main_window.staff_builder.convert_staff_to_grand(
            original_staff,
            new_staff,
            self.parent_page
        )
        
        # Replace the current staff with the grand staff in the parent page's children list
        self.parent_page.children.remove(caller.parent)
        self.parent_page.children.append(grand_staff)       
        
        # change the original staff target control to the new grand staff. This is important for the dialog to know which staff to operate on.
        original_staff.change_action_button_target_control(grand_staff)

        # Once converted to grandstaff, we can now extend it so we need to hide the create button and display the extend button
        original_staff.adjust_staff_generation_buttons()

        # re-adjust the positions of the staffs below the grand staff to accommodate the new grand staff height.
        self.parent_page.order_children() 

    def adjust_staff_generation_buttons(self):
        # Hide create-grand-staff button because we already have a grand staff
        create_grand_staff_button = next((button for button in self.action_buttons if button.action == "convert_to_grand_staff"), None)
        extend_grand_staff_button = next((button for button in self.action_buttons if button.action == "extend_grand_staff"), None)

        # we assume that these buttons must be available for a visible grand staff.
        if create_grand_staff_button:
            create_grand_staff_button.hide()

        if extend_grand_staff_button:
            extend_grand_staff_button.show()    

    """
        This is to be called on first staff of grand staff only. Cause subsequent staves don't affect the grand staff.
    """
    def point_action_to_parent_grand_staff(self, grand_staff):
        for button in self.action_buttons:
            button.change_target_control(grand_staff)

    def set_clef(self, new_clef):
        self.clef = new_clef
        existing_clefs = self.get_children_of_instance(Clef)

        for existing_clef in existing_clefs:
            if existing_clef in self.children:
                self.children.remove(existing_clef)

        self.add_child(new_clef)

    def set_key_signature(self, key):
        self.key_signature = key

    def __str__(self):
        lines_str = "-> ".join(str(line) for line in self.lines)
        intervals_str = "-> ".join(str(interval) for interval in self.intervals)
        virtual_lines_str = "-> ".join(str(line) for line in self.virtual_lines)
        virtual_intervals_str = "-> ".join(str(interval) for interval in self.virtual_intervals)

        return (f"clef: {self.clef} - time_signature: {self.time_signature} - key_signature: {self.key_signature} - "
                f"Top:{self.top_position.x, self.top_position.y} - Bottom:{self.bottom_position.x, self.bottom_position.y} -"
                f"\n- lines: [{lines_str}]" 
                f"\n- Virtual lines: [{virtual_lines_str}]" 
                f"\n- intervals: [{intervals_str}]"
                f"\n- Virtual intervals: [{virtual_intervals_str}]")


