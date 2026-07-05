
from Model.Geometry.Position import Position
from Model.Score.Note import Note
from Model.Score.StaffItem import StaffItem


class Interval(StaffItem):
    def __init__(self, position_rect, 
                 key, key_id, is_virtual, vertical_positioning, 
                 staff_index, line_collateral_boundaries, velocity, tempo, parent_staff):

        super().__init__(
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

        self.position_rect = position_rect

    def get_rect(self):
        return self.position_rect.get_rect()

    def get_position_rect(self):
        return self.position_rect
    
    def add_note(self, note):
        self.notes.append(note)

    """
        Thickness will be highest y - lowest y + 1 because we count thickness as no of pixels. e.g. 140 to 149
    """
    def get_thickness(self):
        return self.position_rect.bottom_left.y - self.position_rect.top_left.y + 1

    """ Checks if point is contained within an interval. """
    def contains_position(self, position):
        return ((self.position_rect.top_left.x <= position.x <= self.position_rect.top_right.x) 
            and (self.position_rect.top_left.y <= position.y <= self.position_rect.bottom_left.y))

    def is_within_collateral_boundaries(self, position):
        return self.line_collateral_boundaries.left_boundary <= position.x <= self.line_collateral_boundaries.right_boundary
    
    """
        Checks if mouse position is within interval but leaving a threshold/padding if specified
    """
    def mouse_hovering_around(self, mouse_position, vertical_threshold=0):        
        return (self.is_within_collateral_boundaries(mouse_position) and
             (self.position_rect.top_left.y + vertical_threshold <= mouse_position.y 
              <= self.position_rect.bottom_left.y - vertical_threshold))    

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
      
    def add_note_at_position(self, position, duration) -> Note:
        # Adjust position to be position of line 
        y_offset =  ((self.position_rect.bottom_left.y - self.position_rect.top_left.y) // 2)
        note_position = Position(position.x, self.position_rect.top_left.y + y_offset)        
        new_note = Note(self, duration, note_position, self.get_next_note_index(), False, 
                        self.key, self.key_id, self.tempo, self.velocity)        
        new_note.set_parent(self)
        self.add_note(new_note)  
        return new_note
     
    def move(self, offset_x:int, offset_y:int):
        self.position_rect.move(offset_x, offset_y)
        
    def move_y(self, offset_y:int):
        self.position_rect.move_y(offset_y)

    def __str__(self):
        return (f"\n{"Virtual " if self.is_virtual else ""}Interval #{self.staff_index} - Key id: {self.key_id} - Vertical positioning: {self.vertical_positioning} - Top-Left{self.position_rect.top_left} - Top-Right: {self.position_rect} "
                f"- Bottom-Left: {self.position_rect.bottom_left} - Bottom-Right: {self.position_rect.bottom_right}"
                )