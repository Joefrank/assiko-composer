

from Model.Score.NoteItemsList import NoteItemsList


class StaffNoteItems:   
    def __init__(self, top_of_staff_notes: NoteItemsList, staff_notes: NoteItemsList, bottom_of_staff_notes: NoteItemsList):
        self.top_of_staff_notes: NoteItemsList = top_of_staff_notes
        self.staff_notes: NoteItemsList = staff_notes
        self.bottom_of_staff_notes: NoteItemsList = bottom_of_staff_notes