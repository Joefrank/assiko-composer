

import copy

from Model.Score.Chord import Chord

class GrandStaff:   
   
    def __init__(self, staves=None, top_left = (0, 0), bottom_right = (0, 0)):
        if staves is None:
            self.staves = []
        self.staves = staves
        self.top_left_position = top_left
        self.bottom_right_position = bottom_right

    def add_staff(self, staff):
        self.staves.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left

    def set_bottom_right_position(self, bottom_right):
        self.bottom_right_position = bottom_right

    def find_nearest_note(self, position):
        for staff in self.staves:
            note = staff.find_nearest_note(position)
            if note is not None:
                return note
        return None

    def get_top_left(self):
        if len(self.staves) > 0:
            return self.staves[0].get_top_left()
        
    def get_bottom_left(self):        
        no_of_staves = len(self.staves)
        if no_of_staves > 0:
            return self.staves[no_of_staves - 1].get_bottom_left()
        
    def get_notes(self):
        notes = []
        for staff in self.staves:
            notes.extend(staff.get_notes())
        return notes
    
    def get_notes_offsets(self):
        if len(self.staves) > 0:
            return self.staves[0].get_notes_offsets()
        
    def get_chords(self):
        chords = list[Chord]()
        staff_count = 0
        for staff in self.staves:
            if staff_count == 0:
                chords.extend(staff.get_chords())
            else:
                staff_chords = staff.get_chords()
                for chord in staff_chords:
                    # find if chord with same x exists
                    existing_chord = next((c for c in chords if c.x_offset == chord.x_offset), None)
                    if existing_chord is not None:
                        # add notes to existing chord
                        existing_chord.append_chord(chord)
                    else:
                        chords.append(chord)
            staff_count += 1
        # sort all chords by x position
        chords.sort(key=lambda c: c.x_offset)
        return chords
    
    def get_initial_navigator_line(self):
        top_staff_top, _ = self.staves[0].get_initial_navigator_line()
        _, bottom_staff_bottom = self.staves[-1].get_initial_navigator_line() 
        top_left = copy.deepcopy(top_staff_top)
        bottom_left = copy.deepcopy(bottom_staff_bottom)
        return (top_left, bottom_left)
    
    def find_nearest_item_to_position(self, position):        
        for staff in self.staves:
            nearest_item = staff.find_nearest_item_to_position(position)
            if nearest_item is not None:
                return nearest_item
          
        return None
    