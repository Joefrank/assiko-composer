
from DataClasses.Config.ScreenConfig import StaffConfig
from DataClasses.Config.MusicConfig import (AccidentalOptions, NoteDurationInTicks, 
             NoteOptions, note_modifiers)
from Model.Geometry import Position
from Model.Score.Helpers.StaffUtils import StaffUtils

class Note:

    """
        duration: how long is the note for
        position: position on the staff item
        order: order on the staff item
        extended: if note duration is extended
        key: the related music note/key name that is for this object
        key_id: the exact piano music key to be played for this note
        beam_width: if this note has another key it is connected with.
    """
    def __init__(self, staff_item, duration, position, order, extended, key, key_id, beam_with=None, 
                 tempo=80, velocity=60):
        self.staff_item = staff_item
        self.duration:tuple = duration # in beats
        self.position:Position = position # position to center rest around
        self.order:int = order
        self.extended:bool = extended
        self.staccato:bool = None
        self.velocity:int = velocity # this is intensity of the note. e.g. Piano, Forte, Fortissimo
        self.tempo:int = tempo # this is used to calculate the duration of the note.
        self.key:str = key
        self.key_id:str = key_id
        self.key_value:int = StaffUtils.get_key_code_from_keyid(key_id)
        self.beam_with:Note = beam_with # this is when we link to another note
        self.connected_note:Note = None
        self.stem_inverted = False
        self.color = None
        self.is_being_played = False
        self.accidental = None

    """
        staff_item: line/interval containing this note
    """
    def set_parent(self, staff_item):
        self.staff_item = staff_item

    def get_parent(self):
        return self.staff_item
    
    def get_accidental(self):
        return self.accidental
    
    def set_accidental(self, accidental):
        self.accidental = accidental

    def implement_unary_modifier(self, modifier):
        modifier_key = modifier[0].lower()
        
        if not modifier_key in note_modifiers:
            return

        match modifier_key:
            case 's':                 
                 self.staccato = True
            case 'x':
                 self.extended = True            
            case 'd':
                 self.staff_item.delete_note(self)           
            case 'i':
                 self.stem_inverted = not self.stem_inverted
            case 'f':
                 self.accidental = AccidentalOptions.FLAT    
            case '#':
                 self.accidental = AccidentalOptions.SHARP
            case 'n':
                 self.accidental = AccidentalOptions.NATURAL
            case 'df':
                 self.accidental = AccidentalOptions.DOUBLE_FLAT
            case 'd#':
                 self.accidental = AccidentalOptions.DOUBLE_SHARP

    def implement_binary_modifier(self, modifier, linked_note):
        if modifier not in note_modifiers:
            return

        match modifier:           
            case 'b':
                 self.beam_with = linked_note          
            case 'c':
                 self.connected_note = linked_note 

    def is_near_position(self, position: Position) -> bool:
         proximity_threshold = StaffConfig.NOTE_PROXIMITY_THRESHOLD // 2
         return ((self.position.x - proximity_threshold <= position.x <= self.position.x + proximity_threshold)
             and (self.position.y - proximity_threshold <= position.y <= self.position.y + proximity_threshold))

    def get_distance_to(self, position:Position):
        return (self.position.x - position.x)**2 + (self.position.y - position.y)**2
    
    def get_exact_duration(self):
        duration = self.duration[4] * 1.5 if self.extended else self.duration[4] 
        exact_duration = duration       
        rest_duration = 0

        if self.staccato: # staccato is 1/4 of one tick
            exact_duration = NoteDurationInTicks.QUARTER * 0.25
            rest_duration = (duration - exact_duration) if duration > NoteDurationInTicks.QUARTER else 0
              
        return exact_duration, rest_duration
    
    def get_velocity(self):
        return self.velocity
    
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def get_tempo(self):
        return self.tempo
    
    def set_tempo(self, tempo):
        self.tempo = tempo
    
    def highlight(self, color):
        self.color = color
    
    def is_in_play(self):
        return self.is_being_played
    
    def set_in_play(self):
        self.is_being_played = True

    def set_off_play(self):
        self.is_being_played = False
        
    def get_head_font_code(self):
        if self.duration[4] <= NoteDurationInTicks.QUARTER:  # Quarter note or shorter
            return NoteOptions.BLACKNOTEHEAD  # Black note head
        else: 
            return NoteOptions.WHITENOTEHEAD  # White note head

    def __str__(self):
        return f"Note {self.key_id} - Position:{self.position} - Order: {self.order} - Extended:{self.extended}" + \
            f" Staccato:{self.staccato} - Duration: {self.duration}"