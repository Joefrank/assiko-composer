
from DataClasses.Config.MusicConfig import (MODULATION_FLAT, MODULATION_SHARP, MODULATION_SHARP_KEY, NoteModifierDetails, 
    piano_notes_sharps, piano_notes_flats, lowest_note_code, note_modifiers)
from Model.Geometry.Position import Position
from Model.Score.GrandStaff import GrandStaff


class StaffUtils:

    @staticmethod
    def find_key_signature_modulation(key_signature, modulations):
        for category, data in modulations.items():
            if key_signature in data["key_signatures"]:
                return category, data
        return None, None

    @staticmethod
    def resolve_position_with_margins(position, margins):       
        x = position[0] + margins[0] - margins[2]
        y = position[1] + margins[1] - margins[3]  
        return Position(x, y)

    @staticmethod
    def get_signature_item_coordinates_for_interval(line_gap, modulation_item_index, modulation_size, lines, intervals,
                                                    item_position_index, modulation_item_spacing, modulations_x_offset):
        """
        Calculates the Y-position for key signature items outside the standard 5-line staff.
        """
        half_line_gap = (line_gap // 2)
        # Only handle positions outside the staff (above or below)
        if item_position_index < 1:
            start_position = lines[0].start_position
            offset = half_line_gap + (line_gap * item_position_index)  # Top line
        elif item_position_index > 4:
            start_position = lines[4].start_position
            offset = (line_gap * (item_position_index - 4)) - half_line_gap # bottom line
        else:
            start_position = intervals[item_position_index-1].position_rect.top_left
            offset = half_line_gap

        y_offset = start_position.y + offset
        x_offset = modulations_x_offset +  (modulation_item_index * (modulation_item_spacing))
        return Position(x_offset, y_offset)

    @staticmethod
    def get_signature_item_coordinates_for_line(line_gap, modulation_item_index, modulation_size, lines, item_position_index,
                                                modulation_item_spacing, modulations_x_offset):
        """
        Calculates the Y-position for key signature items outside the standard 5-line staff.
        """
        # Only handle positions outside the staff (above or below)
        if item_position_index < 1:
            line = lines[0]
            start_position = line.start_position
            offset = line_gap * item_position_index  # Top line
        elif item_position_index > 5:
            line = lines[4]
            start_position = line.start_position
            offset = line_gap * item_position_index # bottom line
        else:
            line = lines[item_position_index-1]
            start_position = line.start_position
            offset = 0
        
        y_offset = start_position.y + offset
        x_offset = modulations_x_offset +  (modulation_item_index * (modulation_item_spacing))
        
        return Position(x_offset, y_offset) #, line

    @staticmethod
    def calculate_score_dimension(music_score):
        from Model.Score.Staff import Staff
        height, width = (0, 0)
        all_staves = music_score.staves_sequence
        
        for staff in all_staves:
            if isinstance(staff, Staff):
                height += staff.bottom_position.y - staff.top_position.y
                width = staff.lines[0].end_position.x - staff.lines[0].start_position.x
            elif isinstance(staff, GrandStaff):
                height += staff.bottom_right_position.y - staff.top_left_position.y
                width = staff.bottom_right_position.x - staff.top_left_position.x

        return width, height
    
    @staticmethod
    def get_all_notes_by_modulation(modulation_type):
        if modulation_type == MODULATION_SHARP:  # modulate note
            return piano_notes_sharps
        elif modulation_type == MODULATION_FLAT:
            return piano_notes_flats
        else:
            return None
        
    @staticmethod
    def get_all_notes_by_modulation_key(modulation_key):        
        if modulation_key == MODULATION_SHARP_KEY:  # modulate note
            return piano_notes_sharps
        else: 
            return piano_notes_flats
        
    @staticmethod
    def get_key_code_from_keyid(key_id):
        if len(key_id) == 3:
            modulation_key = key_id[2]
        else:
            modulation_key = None

        piano_notes = StaffUtils.get_all_notes_by_modulation_key(modulation_key)
        key_index = piano_notes.index(key_id)     
        return lowest_note_code + key_index  
        
    @staticmethod
    def get_modifier_by_key(key):
        if key not in note_modifiers:
            return None
        
        match key.lower():
            case 's':                 
                 return NoteModifierDetails.STACCATO
            case 'x':
                 return NoteModifierDetails.EXTEND
            case 'b':
                 return NoteModifierDetails.BEAM
            case 'd':
                 return NoteModifierDetails.DELETE
            case 'c':
                 return NoteModifierDetails.CONNECT
            case 'i':
                 return NoteModifierDetails.INVERT_STEM
            case 'l':
                 return NoteModifierDetails.LINK
            case 'f':
                 return NoteModifierDetails.FLAT    
            case '#':
                 return NoteModifierDetails.SHARP
            case 'n':
                 return NoteModifierDetails.NATURAL
            case 'df':
                 return NoteModifierDetails.DOUBLE_FLAT
            case 'd#':
                 return NoteModifierDetails.DOUBLE_SHARP
        return None