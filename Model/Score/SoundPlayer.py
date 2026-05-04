import queue
import threading
import mido
import time
from DataClasses.Config.MusicConfig import NoteDurationInTicks, SoundPlayerEventConstants
from Model.Score.Chord import Chord
from Model.Score.Helpers.MusicUtils import MusicUtils
from Model.Score.Note import Note
from Model.Score.PianoNote import PianoNote


class SoundPlayer:
    keys_played = []
    
    def __init__(self):
        self.outport = mido.open_output()
        self.note_queue = queue.Queue()
        self.chord_queue = queue.Queue()
        self.play_lock = threading.Lock()
        self.feedback_queue = queue.Queue()
        self.pending_chord_queue = queue.Queue()

        self.midi_thread = threading.Thread(
            target=self.midi_worker,
            daemon=True
        )
        self.midi_thread.start()

        self.pending_chord_thread = threading.Thread(
            target=self.terminate_pending_notes,
            daemon=True
        )
        self.pending_chord_thread.start()

    def play_key(self, key_code):
        self.keys_played.append(key_code)
        self.outport.send(mido.Message('note_on', note=key_code, velocity=127))
        time.sleep(0.2)
    
    """
        Playing note with specific duration is done with note_on and note_off then 
        putting the delay in between the two.
        note_key_code: is the number representing the note between 21 and 109 - 88 key on piano
        duration_ticks: is the duration of the note
        velocity: Controls loudness / brightness (0 - 127)
    """
    def play_note(self, note_key_code, duration_ticks, velocity=60, tempo=80):
        try:
            self.outport.send(mido.Message('note_on', note=note_key_code, velocity=velocity))
            duration = MusicUtils.get_note_duration(duration_ticks, tempo)
            time.sleep(duration)
            self.outport.send(mido.Message('note_off', note=note_key_code, velocity=velocity))
        except IOError:
            print("Could not open MIDI output. Available ports:")
            print(mido.get_output_names())

    """
        Plays piano note with a delay to match timing/duration
    """
    def play_piano_note(self, velocity, tempo, note=60, duration_in_ticks=NoteDurationInTicks.QUARTER, channel=0):
        # Note ON
        note_on = mido.Message('note_on', note=note, velocity=velocity, channel=channel, program=32)
        self.outport.send(note_on)
        
        # Wait for note duration
        duration_in_seconds = MusicUtils.get_note_duration(duration_in_ticks, tempo)
        time.sleep(duration_in_seconds)

        # Note OFF
        note_off = mido.Message('note_off', note=note, velocity=0, channel=channel)
        self.outport.send(note_off)
        
    def play_note_crescendo(self, note_key_code, duration_ticks, cresendo_steps, tempo):
        for velocity in range(len(cresendo_steps)):  # [40, 60, 80, 100]
            self.play_note(note_key_code, duration_ticks, velocity, tempo)

    def midi_worker(self, port_name='Microsoft GS Wavetable Synth'):
         try:     
              pending_notes = None         
              while True:
                # if self.chord_queue.qsize() == 0:
                #     continue
                chord = self.chord_queue.get()  # blocks until a chord is available   

                with self.play_lock:  
                    self.feedback_queue.put((SoundPlayerEventConstants.CHORD_START, chord))  # Notifies UI thread of update         
                    pending_notes = self.play_chord(chord)  
                    if pending_notes is not None:
                        self.add_pending_notes_to_queue(pending_notes)
                    self.feedback_queue.put((SoundPlayerEventConstants.CHORD_END, chord))                 
                self.chord_queue.task_done()  

                if self.chord_queue.qsize() == 0:
                    self.feedback_queue.put((SoundPlayerEventConstants.BATCH_END, chord))                             

         except queue.Empty:
             print("Queue is empty, waiting for new chords...")
             print(mido.get_output_names())
             
         finally: # clean up
            if self.outport:
                # Safety: turn off any stuck notes
                for note in range(128):
                    self.outport.send(mido.Message('note_off', note=note, velocity=0))

                self.outport.close()

    def play_chord(self, chord: Chord):
        chord.set_notes_in_play()
        note_details = chord.get_playable_notes()        
        notes = self.group_notes_by_duration(note_details)
        smallest_duration = notes[0].duration_in_seconds

        #print("------------------------------------starting --------------------")
        for note in notes:
            if note.duration_in_seconds < smallest_duration: # find smallest duration
                smallest_duration = note.duration_in_seconds

            self.outport.send(mido.Message('note_on', note=note.key_code, velocity=note.velocity))            
        
        time.sleep(smallest_duration)

        #print("------------------------------------Terminating --------------------")
        for note in notes:
            if note.duration_in_seconds == smallest_duration: # only stop notes that have reached their duration
                self.outport.send(mido.Message('note_off', note=note.key_code))
                note.note.set_off_play()
                notes.remove(note)  # remove note from list as it has finished playing
        
        # reduce remaining notes duration
        for note in notes:
            note.duration_in_seconds -= smallest_duration

        # pending notes will be returned and further processed
        return notes if len(notes) > 0 else None
    
    def add_pending_notes_to_queue(self, notes: list[PianoNote]):
        self.pending_chord_queue.put(notes)

    def terminate_pending_notes(self): # type: ignore
         try:     
                     
              while True:                
                pending_notes = self.pending_chord_queue.get()  # blocks until a chord is available   
                notes_to_terminate = []

                # get the next smallest duration
                while len(pending_notes) > 0:
                    smallest_note_in_duration = min(pending_notes, key=lambda note: note.duration_in_seconds)
                    time.sleep(smallest_note_in_duration.duration_in_seconds)
                    for note in pending_notes:
                        if note.duration_in_seconds == smallest_note_in_duration.duration_in_seconds:
                            self.outport.send(mido.Message('note_off', note=note.key_code))
                            note.note.set_off_play()
                            notes_to_terminate.append(note.note)
                            pending_notes.remove(note)                            
                           
                    self.feedback_queue.put((SoundPlayerEventConstants.PENDING_CHORD_END, notes_to_terminate))
                    
                    # for any remaining notes, reduce their duration
                    for note in pending_notes:
                        note.duration_in_seconds -= smallest_note_in_duration.duration_in_seconds                   
                                    
                self.pending_chord_queue.task_done()

         except queue.Empty:
             print("Queue is empty, waiting for new chords...")
             print(mido.get_output_names())


    def group_notes_by_duration(self, notes: list[tuple[int, int, int, int, Note]]) -> []: # type: ignore      
        piano_chords = []
        duration_dict = []       
        chord_order = 1
        
        for piano_note in piano_chords:
            piano_note.sort_out_duration(duration_dict)

        for note in notes:
            duration = MusicUtils.get_note_duration(note[1], note[3])
            piano_note = PianoNote(note[0], duration, note[2], chord_order, note[4])
            piano_chords.append(piano_note)
            if duration not in duration_dict:
                duration_dict.append(duration)            
            chord_order += 1
        
       
        return piano_chords
   
   
    def add_note_to_queue(self, note, length):
        self.note_queue.put((note, length))

    def add_chord_to_queue(self, chord: Chord):       
        self.chord_queue.put(chord)

    def add_chords_to_queue(self, chords: list[Chord]):       
        for chord in chords:
            self.chord_queue.put(chord)

   