
from DataClasses.Config.MusicConfig import TICKS_PER_BEAT


class MusicUtils:    
    
     """ This duration (in seconds) is to be passed to the mido output for notes timing. """
     @staticmethod
     def get_note_duration(duration_in_ticks:int, tempo:int) -> float:
        seconds_per_beat = 60 / tempo
        seconds_per_tick = seconds_per_beat / TICKS_PER_BEAT
        return duration_in_ticks * seconds_per_tick
    

