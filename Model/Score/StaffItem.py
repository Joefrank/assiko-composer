

""" Class acts as parent class for Line and Interval """

from Model.Score.Note import Note


class StaffItem:
    def __init__(self, staff_index, key, key_id, is_virtual, vertical_positioning, 
                 line_collateral_boundaries, velocity, tempo, parent_staff, **kwargs):
        super().__init__(**kwargs)
        self.staff_index = staff_index
        self.key = key
        self.key_id = key_id
        self.is_virtual = is_virtual
        self.vertical_positioning = vertical_positioning
        self.line_collateral_boundaries = line_collateral_boundaries
        self.velocity: int = velocity
        self.tempo: int = tempo
        self.notes = []
        self.parent_staff = parent_staff
        self.app_state = None


    def set_parent_staff(self, parent_staff):
        self.parent_staff = parent_staff

    def set_staff_index(self, staff_index):
        self.staff_index = staff_index   

    def get_notes(self, x_offset=None) -> list[Note]:
        return [
            note for note in self.notes
            if x_offset is None or note.position.x == x_offset
    ] 

    def delete(self):
        if self.parent_staff == None:
            return
        
        self.parent_staff.unlink(self)
        self.parent_staff = None

    def set_app_state(self, app_state):        
        if self.app_state is None:
            self.app_state = app_state
        
       

