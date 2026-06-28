
from copy import copy
from typing import List

from pygame import Surface

from DataClasses.Config.ScreenConfig import Color, MouseEventType
from DataClasses.Config.MusicConfig import valid_note_durations, note_modifiers, default_note_duration

from Model.Events.MouseEvent import MouseEvent
from Model.Score.Chord import Chord
from Model.Score.Helpers.StaffUtils import StaffUtils
from Model.Score.Helpers.StaffUtils import StaffUtils
from Model.Score.MusicScore import MusicScore
from Model.Score.Note import Note
from Model.Score.SoundPlayer import SoundPlayer
from Model.Score.Staff import Staff
from Model.Score.Staff import Staff


class ApplicationState:
    """Manages the current state of the application.""" 

    def __init__(self, main_window):
        self.screen = main_window.screen
        self.pending_dropped_item = None
        self.sound_player = SoundPlayer() 
        self.staff_renderer = None
        self.screen_renderer = None
        self.is_running: bool = True
        self.screen_needs_refresh = False
        self.music_score = None
        self.music_score_backup = None #used to reset score
        self.error_messages = List[str]
        self.last_note_added = None        
        self.note_duration = None
        self.keys_down = ''
        self.note_modifier = None
        self.main_menu = None
        self.screen_width = None
        self.screen_height = None
        self.mouse_click = MouseEvent(MouseEventType.CLICK)
        self.mouse_hover = MouseEvent(MouseEventType.HOVER)
        self.score_navigator = None
        self.events_queue = []
        self.pending_chord: Chord = None
        self.main_window = main_window
        self.main_window_event_handler = main_window.get_event_handler()

    def get_main_window(self):
        return self.main_window
    
    def get_window_event_handler(self):
        return self.main_window_event_handler
     
    def save_dropped_symbol(self, rect, action, params_input):
        self.pending_dropped_item = (rect, action, params_input)

    def get_dropped_symbol(self):
        return self.pending_dropped_item
       
    def clear_dropped_symbol(self):
        self.pending_dropped_item = None

    def raise_screen_update_event(self):
        print("Raising screen update event")
        # screen_update_event = ScreenUpdateEvent()
        # screen_update_event.register(self)
        # self.events_queue.append(screen_update_event)

    def screen_update_needed(self) -> bool:
        self.screen_needs_refresh = True
    
    def set_screen_refresh_status(self, needs_refresh: bool):
        self.screen_needs_refresh = needs_refresh

    def get_next_event(self):
        if len(self.events_queue) == 0:
            return None
        return self.events_queue.pop(0)
    
    def set_renderers(self, staff_renderer, screen_renderer):
        self.staff_renderer = staff_renderer
        self.screen_renderer = screen_renderer

    def set_main_screen(self, screen: Surface):
        self.main_canvass = screen
        
   
    def set_music_score(self, score: MusicScore):
        self.music_score = score
        self.music_score_backup = copy.deepcopy(score)

    def set_score_navigator(self, score_navigator):
        self.score_navigator = score_navigator

    def set_last_added_note(self, note: Note):
        self.last_note_added = note
    
    def add_error(self, message: str) -> None:
       # """Add an error message to the queue."""
        self.error_messages.append(message)

    def get_and_clear_errors(self) -> List[str]:
       """Get all error messages and clear the queue."""
       errors = self.error_messages.copy()
       self.error_messages.clear()
       return errors
    
    """ Registers key down as note duration."""
    def register_key_down(self, key_name):   
        self.keys_down += key_name
        if self.keys_down.isnumeric(): # this is potentially a key duration
            note_duration_details = next((item for item in valid_note_durations if item[0] == key_name), None)
            # At this stage, we only register note duration details.
            if note_duration_details is not None:
                self.note_duration = note_duration_details # this is font code
        elif self.keys_down in note_modifiers:
            self.note_modifier = StaffUtils.get_modifier_by_key(self.keys_down)          
            # We want to clear the mouse tracking for any note modifier 
            # TODO: leave tracker until you come to close to a existing note
            if self.note_modifier is not None:
                self.hide_mouse_tracker()
        print(f"Registered keys down: {self.keys_down}")
    
    def hide_mouse_tracker(self):
        self.mouse_hover.reset_current_position()                   
        self.set_screen_refresh_status(True)      
    
    def handle_pending_events(self):
        # TODO: play the pending chord and record it
        if self.pending_chord is not None:
            self.sound_player.play_chord(self.pending_chord)
            self.pending_chord = None

    def cancel_key_down(self):
        self.note_duration = None
        self.note_modifier = None
        self.keys_down = ''

    def get_registered_key(self):
        return self.note_duration
    
    def get_registered_note_modifier(self):
        return self.note_modifier
    
    def find_nearest_note_to_position(self, position) -> Note:
        for staff in self.music_score.staves_sequence:
            nearest_note = staff.find_nearest_note(position)
            if nearest_note is not None:
                return nearest_note
        return None   
    
    def find_nearest_staff_item_to_position(self, position) -> Staff:
        return self.music_score.find_nearest_staff_item(position)
    
    def effect_note_modifier(self, note: Note, modifier):        
        if modifier[1] == 1:
            note.implement_unary_modifier(modifier)
        elif modifier[1] == 2:
            note.implement_binary_modifier(modifier)
        elif modifier[1].lower() == 'x':          
            if self.pending_chord is None:
                self.pending_chord = Chord("", note.position.x)           
            self.pending_chord.add_note(note)  

    def register_mouse_over_event(self, new_mouse_position):
        self.mouse_hover.set_current_position(new_mouse_position)
        self.mouse_hover.notify()

    """ Registers a mouse click. If a staff item is found near the click position, and there is not a note modifier,
        we add a note to the staff item as new note. If there is a note modifier, we apply the modifier to the nearest note found.
    """
    def register_mouse_click_event(self, new_mouse_position):
        if new_mouse_position is None: # mouse position must be valid
            return
        
        # If there is a note modifier, we apply it to the nearest note found
        if self.note_modifier is not None:
            nearest_note = self.find_nearest_note_to_position(new_mouse_position)
            if nearest_note is not None:
                self.effect_note_modifier(nearest_note, self.note_modifier)
        # If no note modifier, we try to add a new note to the nearest staff item
        else:
            nearest_staff_item = self.music_score.find_nearest_staff_item_to_position(new_mouse_position)
            if nearest_staff_item is not None: # staff item is either line or interval             
                self.add_note_to_staff_item(nearest_staff_item, new_mouse_position)
            else: # just register the click position
                self.mouse_click.set_current_position(new_mouse_position)

        self.mouse_click.set_current_position(new_mouse_position)
        self.mouse_click.notify()

    def add_note_to_staff_item(self, nearest_staff_item, position):
        note_duration = default_note_duration if self.note_duration is None else self.note_duration
        new_note = nearest_staff_item.add_note_at_position(position, note_duration)
        self.set_last_added_note(new_note)
        note_key_code = StaffUtils.get_key_code_from_keyid(new_note.key_id)
        note_duration, rest_duration = new_note.get_exact_duration()
        self.sound_player.play_note(note_key_code, note_duration, new_note.velocity, new_note.tempo)
        if rest_duration > 0:
            self.sound_player.play_note(0, rest_duration, 0, new_note.tempo)  # 0 key_value for rest
    
  
    def highlight_chord(self, chord: Chord, highlight: bool):       
        for note in chord.notes:
            
            if not highlight and not note.is_in_play():
                color = Color.BLACK
            else:
                color = Color.PINK
           
            note.highlight(color)
        self.set_screen_refresh_status(True)

    def clear_pending_notes(self, notes: list[Note]):
        for note in notes:
            note.highlight(Color.BLACK)
        self.set_screen_refresh_status(True)