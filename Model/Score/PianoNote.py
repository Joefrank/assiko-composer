

from Model.Score.Note import Note


class PianoNote:
    
    """Class representing a piano note."""
    def __init__(self, key_code, duration_in_seconds, velocity, chord_order, note: Note):
        self.key_code = key_code
        self.duration_in_seconds = duration_in_seconds
        self.velocity = velocity
        self.chord_order = chord_order
        self.duration_breakdown = []
        self.note = note

    def sort_out_duration(self, duration_dict):
        if len(duration_dict) <= 2:
            return
        
        for duration in sorted(duration_dict):
            if self.duration_in_seconds > duration:
                self.duration_breakdown.append(duration)