class MusicScore:
    TICKS_PER_BEAT = 480
    
    def __init__(self, top_left, score_width=None, title=None, credits=None, tempo=80):        
        self.staves_sequence = [] #combination of all GrandStaves, could also be simple staffs         
        self.staff_color = None
        self.key_signature_list = None
        self.title_position = None
        self.highest_credit_y_offset = None
        self.credits = [] # array of text blocks to be added to the top of score apart from title.        
        self.lyrics = []
        self.top_left_position = top_left
        self.score_width = score_width
        self.title = title
        self.raw_credits = credits # these need processing    
      
     
    def add_staff(self, staff):
        self.staves_sequence.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left   

    def set_score_width(self, score_width):
        self.score_width = score_width

    def get_all_notes_in_positional_order(self):
        notes = []
        for staff in self.staves_sequence:
            notes.extend(staff.get_notes())
        return sorted(notes, key=lambda note: note.position.x)
    
    def find_nearest_staff_item_to_position(self, position):        
        for staff in self.staves_sequence:
            nearest_item = staff.find_nearest_item_to_position(position)
            if nearest_item is not None:
                return nearest_item
          
        return None  

    def CreateStaff(self, params_input):
        # Placeholder for staff creation logic
        print("Creating staff..from score..." + params_input) 