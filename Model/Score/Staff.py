from DataClasses.Config.ScreenConfig import StaffConfig
from DataClasses.Config.MusicConfig import supported_time_signatures,TREBLE_CLEF, BARITON_CLEF
from Model.Geometry.Position import Position
from Model.Geometry.Line import Line
from Model.Score.IntervalRect import IntervalRect
from Model.Score.Note import Note
from Model.Score.StaffBar import StaffBar

class Staff:   
    
    def __init__(self, clef=None, time_signature=None, key_signature=None, tempo:int=None, velocity:int=None):       
         # lines and intervals
        self.lines = [] 
        self.intervals = []
        self.virtual_lines = [] # any lines above or below staff
        self.virtual_intervals = [] #any interval above or below staff
         # position attributes
        self.position_rect = None
        self.top_position = None #postion of top line of staff
        self.bottom_position = None #position of bottom line of staff
        self.bottom_line = None # not necessary a line on the staff but how far below you can go with the ledger
        self.top_line = None # not necessary a line on the staff but how far above you can go with the ledger        
        # note boundaries attributes
        self.notes_left_offset = 0 # this is the left boundary for notes on this staff.
        self.notes_right_offset = 0 # this is the right boundary for notes on this staff.
        self.notes_top_offset = 0 # top boundary for notes belonging to this staff
        self.notes_bottom_offset = 0 # bottom boundary for notes belonging to this staff
         # other staff components
        self.modulations = []
        self.bars = []
        self.step_notes_rests_lyrics = []  # these are chords played in steps. It's a list of StaffStep
        self.dynamics = [] # use StaffDynamic as a list
        self.lyrics_lines = []
        # values from constructor parameters
        self.clef = clef
        self.time_signature = time_signature
        self.key_signature = key_signature
        self.velocity:int = velocity
        self.tempo:int = tempo        
      
    def set_notes_boundaries(self):
        self.notes_left_offset = self.top_line.line_collateral_boundaries.left_boundary
        self.notes_right_offset = self.top_line.line_collateral_boundaries.right_boundary
        self.notes_top_offset = self.top_line.start_position.y
        self.notes_bottom_offset = self.bottom_line.start_position.y

    def get_width(self):
        return self.top_line.end_position.x - self.top_line.start_position.x
    
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
    
    def set_positions(self):       
        self.top_line = self.lines[0]
        self.bottom_line = self.lines[-1]
        self.position_rect = IntervalRect(self.top_line.start_position,  self.top_line.end_position,
                                        self.bottom_line.end_position, self.bottom_line.start_position)
        self.top_position = self.top_line.start_position
        self.bottom_position = self.bottom_line.start_position  
    
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


