from itertools import zip_longest
from Configs.music_config import (supported_clef_settings, piano_notes_sharps, supported_modulations,
                                  MODULATION_SHARP, MODULATION_FLAT, piano_notes_key_patterns, piano_notes_flats)
from Configs.screen_config import VERTICAL_POSITION_BOTTOM, VERTICAL_POSITION_TOP
from Models import NoteItemsList, StaffNoteItems
from Services.Utils import StaffUtils

class StaffNoteBuilder:

    def __init__(self):
        self.supported_clef_settings = supported_clef_settings

    """
        staff_offset_count: no of lines and interval (virtual ones) offset from staff
    """
    def build_staff_notes(self, clef, key_signature, staff_offset_count) -> StaffNoteItems:
        clef_settings = self.supported_clef_settings[clef]
        amplitude_for_lines_and_intervals = staff_offset_count * 2
        modulation_type = next(
            (name for name, details in supported_modulations.items() if key_signature in details["key_signatures"]),
            None
        )
        notes_per_line = self.modulate_staff_notes(clef_settings["notes_per_line"], clef, key_signature, modulation_type)
        notes_per_interval = self.modulate_staff_notes(clef_settings["notes_per_interval"], clef, key_signature, modulation_type)
        staff_note_items = NoteItemsList.NoteItemsList(notes_per_line, notes_per_interval)
        #interval_notes_top, line_notes_top 
        staff_note_items_top = self.modulate_virtual_notes(clef, notes_per_line[-1], amplitude_for_lines_and_intervals,  key_signature,  VERTICAL_POSITION_TOP, modulation_type)
        #interval_notes_bottom, line_notes_bottom 
        staff_note_items_bottom = self.modulate_virtual_notes(clef, notes_per_line[0], amplitude_for_lines_and_intervals, key_signature, VERTICAL_POSITION_BOTTOM, modulation_type)
        return StaffNoteItems.StaffNoteItems(staff_note_items_top, staff_note_items, staff_note_items_bottom)

    def modulate_staff_notes(self, notes, clef, key_signature, modulation_type):
        modulations = self.supported_clef_settings[clef]["signature_position_pattern"][key_signature]
        modulated_notes = [list(d.keys())[0] for d in modulations]
        resulting_notes = []
        unsharpenabled_notes = ['E','B']
        unflattenable_notes = ['C','F']
        
        for note in notes:
            note_char1 = note[0]
            if note_char1 in modulated_notes:                
                modulation_details = next((d for d in modulations if note[0] in d), None)
                if modulation_type == MODULATION_SHARP: # modulate note
                    if note_char1 in unsharpenabled_notes: #we don't sharpen these types, just jump to next note.
                        new_char1 = modulation_details[note_char1][2]
                        if note[0] == 'B':
                            note_index = int(note[1]) + 1
                            new_note = f"{new_char1}{note_index}" 
                        else: 
                            new_note = new_char1 + note[1] 
                    else:
                        new_note = f"{note}#"
                elif modulation_type == MODULATION_FLAT:
                    if note_char1 in unflattenable_notes: #we don't flatten these types, just jump to previous note.
                        new_char1 = modulation_details[note_char1][2]
                        if note[0] == 'C':
                            note_index = int(note[1]) - 1
                            new_note = f"{new_char1}{note_index}"
                        else: 
                            new_note = new_char1 + note[1] 
                    else:
                        new_note = f"{note}b"
                else:
                    new_note = note
                resulting_notes.append(new_note)
            else:
                resulting_notes.append(note)
       
        return resulting_notes

    """
        start_note: note on staff from which we start generating virtual notes 
        modulation_amplitude: number of virtual lines and intervals we are generating around staff vertical padding 
        key_signature: key signature of the staff
        vertical_positioning: top or bottom of staff where we generate virtual notes
        modulation_type: SHARP or FLAT
    """
    def modulate_virtual_notes(self, clef, start_note, modulation_amplitude, key_signature, vertical_positioning,
                               modulation_type):
        key_pattern = piano_notes_key_patterns[modulation_type][key_signature]
        all_notes = StaffUtils.get_all_notes_by_modulation(modulation_type)       

        if all_notes is None:
            return None

        if vertical_positioning == VERTICAL_POSITION_TOP: # in this case, we go from top line note and higher
            factor = 1
        elif vertical_positioning == VERTICAL_POSITION_BOTTOM: # we are going towards deeper notes bass
            factor = -1
        else:
            factor = 0 # go nowhere

        try:
            start_note_index = all_notes.index(start_note) # index in overall notes array.
            start_index_in_pattern = key_pattern.index(start_note_index) # find that index in pattern it must be there
            end_point = start_index_in_pattern + (factor * modulation_amplitude)

            if end_point > start_index_in_pattern:
                start_point = start_index_in_pattern + 1
                end_point += 1
            else:
                start_point = end_point
                end_point = start_index_in_pattern

            pattern_index_chunk = key_pattern[start_point: end_point]
            virtual_notes = [all_notes[i] for i in pattern_index_chunk]
          
            if vertical_positioning == VERTICAL_POSITION_BOTTOM:
                interval_notes = virtual_notes[1::2]  # step = 2, starting at index 0
                line_notes = virtual_notes[::2]  # step = 2, starting at index 1
            else:
                interval_notes = virtual_notes[::2]  # step = 2, starting at index 0
                line_notes = virtual_notes[1::2]  # step = 2, starting at index 1
                
            return NoteItemsList.NoteItemsList(line_notes, interval_notes)

        except ValueError:
            print(f"not found in list")

        return None



