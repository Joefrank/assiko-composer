from Model.Geometry.Line import Line
from Model.Geometry.Position import Position
from Model.Score.Note import Note
from Model.Score.Note import Note
from Model.Score.StaffItem import StaffItem

class StaffLine(Line, StaffItem):
    def __init__(self, 
                 start_position, end_position, thickness, color=(0,0,0), is_virtual=False, key=None, 
                 key_id=None, vertical_positioning=None, staff_index=None, 
                 line_collateral_boundaries=None, velocity=None, tempo=None, parent_staff=None):

        super().__init__(
            start_position=start_position,
            end_position=end_position,
            thickness=thickness,
            color=color,
            staff_index=staff_index,
            key=key,
            key_id=key_id,
            is_virtual=is_virtual,
            vertical_positioning=vertical_positioning,
            line_collateral_boundaries=line_collateral_boundaries,
            velocity=velocity,
            tempo=tempo,
            parent_staff=parent_staff
        )

    def add_note(self, note):
        self.notes.append(note)

    def is_in_vertical_proximity_of_position(self, position, vertical_threshold=0):
        return (self.start_position.y - vertical_threshold) <= position.y <= (self.start_position.y + vertical_threshold)

   
    def is_within_collateral_boundaries(self, position):
        return self.line_collateral_boundaries.left_boundary <= position.x <= self.line_collateral_boundaries.right_boundary
    
    """
        We use this to track mouse 2 pixels around a line.
    """
    def mouse_hovering_around(self, mouse_position, vertical_threshold=0):
        return (self.is_within_collateral_boundaries(mouse_position) and 
                (self.is_in_vertical_proximity_of_position(mouse_position, vertical_threshold) or
                self.contains_position(mouse_position)))
    
    def get_next_note_index(self):
        return len(self.notes)
    
    def delete_note(self, note):
        if note in self.notes:
            self.notes.remove(note)

    def find_nearest_note(self, position):
        for note in self.notes:            
            if note.is_near_position(position):
                return note        
        return None
    
    def get_notes_in_positional_order(self):
        return sorted(self.notes, key=lambda note: note.position.x)          
    
    def add_note_at_position(self, position, duration) -> Note:
        # Adjust position to be position of line        
        note_position = Position(position.x, self.start_position.y) 
        new_note = Note(self, duration, note_position, self.get_next_note_index(), False, 
                        self.key, self.key_id, self.tempo, self.velocity)        
        new_note.set_parent(self)
        self.add_note(new_note)  
        return new_note
    
    def move(self, offset_x, offset_y):
        self.start_position.translateTo(offset_x, offset_y)
        self.end_position.translateTo(offset_x, offset_y)
    
    def move_y(self, offset_y:int):
        self.start_position.translate_y(offset_y)
        self.end_position.translate_y(offset_y)

    def __str__(self):
        return f"\n{"Virtual " if self.is_virtual else ""}Line #{self.staff_index} - Thickness: {self.thickness} - Key id: {self.key_id} - Vertical positioning: {self.vertical_positioning} - Start: {self.start_position} - End: {self.end_position}"