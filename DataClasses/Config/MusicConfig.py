from dataclasses import dataclass

MODULATION_SHARP_KEY = "#"
MODULATION_FLAT_KEY = "b"
MODULATION_SHARP = "MODULATION_SHARP"
MODULATION_FLAT = "MODULATION_FLAT"
TREBLE_CLEF = "TREBLE_CLEF"
BASS_CLEF = "BASS_CLEF"
BARITON_CLEF = "BARITON_CLEF"

TICKS_PER_BEAT = 480

musical_rests = [
    {"name": "Whole rest", "no_of_beats": 4, "font_code": "\uE4E3"},
    {"name": "Half rest", "no_of_beats": 2, "font_code": "\uE4E4"},
    {"name": "Quarter rest", "no_of_beats": 1, "font_code": "\uE4E5"},
    {"name": "Eighth rest", "no_of_beats": 0.5, "font_code": "\uE4E6"},
    {"name": "Sixteenth rest", "no_of_beats": 0.25, "font_code": "\uE4E7"}
]

note_modifiers = ['s','x','b','d','c','i','l','f','#','n','df','d#']

@dataclass
class VelocityLevels:
    PPP: int = 20 # Pianississimo
    PP: int = 40 # Pianissimo
    P: int = 60 # Piano
    MP: int = 80 # Mezzo-piano
    MF: int = 100 # Mezzo-forte
    F: int = 110 # Forte
    FF: int = 120 # Fortissimo
    FFF: int = 127 # Fortississimo

@dataclass
class NoteModifierDetails:
    # format is [list] of keys, no of items affected by modifier
    DELETE = ('d', 1) # delete single note when this key pressed and click on note
    EXTEND = ('x', 1) # extend new/existing note by half its duration on this key press + click 
    STACCATO = ('s', 1) # make new/existing note staccato on key press + click
    INVERT_STEM = ('i', 1) # invert stem of new/existing note on key press + click
    BEAM = ('b', 2) # beem this note to previous if it exist.
    CONNECT = ('c', 2) # connect this note to previous if one exist
    LINK = ('l', 'x') # link notes to create a chord between staves.
    FLAT = ('f', 1) # make note flat
    SHARP = ('#', 1) # make note sharp
    NATURAL = ('n', 1) # make note natural
    DOUBLE_FLAT = ('df', 1) # make note double flat
    DOUBLE_SHARP = ('d#', 1) # make note double sharp

@dataclass
class NoteDurationInTicks:
    WHOLE: int = 1920
    HALF: int = 960
    QUARTER: int = 480
    EIGHT: int = 240
    SIXTHEENTH: int = 120
    THIRTYSECONDTH: int = 60
    SIXTYFOURTH: int = 30 

@dataclass
class NoteOptions:
    STACCATO:str = "\uE4A2"
    BLACKNOTEHEAD:str = "\uE0A4"
    WHITENOTEHEAD:str = "\uE0A3"
    FLAGUP_EIGHT:str = "\uE240"
    FLAGUP_SIXTEENTH:str = "\uE242"
    FLAGDOWN_EIGHT:str = "\uE241"
    FLAGDOWN_SIXTEENTH:str = "\uE243"

@dataclass
class AccidentalOptions:
    SHARP = (0.5, "\uE262")
    FLAT = (-0.5, "\uE260")
    NATURAL = (0.0, "\uE261")
    DOUBLE_SHARP = (1.0, "\uE263")
    DOUBLE_FLAT = (-1.0, "\uE264")

valid_note_durations = \
    [ #(duration, note_type, font_code, stem-on/off, Actual duration)
        ("1","Whole", "\uE0A2",False, NoteDurationInTicks.WHOLE),
        ("2","Half", "\uE0A2", True, NoteDurationInTicks.HALF),
        ("4","Quarter","\uE0A4", True, NoteDurationInTicks.QUARTER),
        ("8","Eighth","\U0001D160", False, NoteDurationInTicks.EIGHT),
        ("0","Sixteenth","\U0001D161", False, NoteDurationInTicks.SIXTHEENTH)
    ]

default_note_duration = next((item for item in valid_note_durations if item[0] == "4"), None)

supported_time_signatures = {
    "2x2":{"fraction" : (2,2), "symbol" : ("\uE082","\uE082"), "size":40, "margins": (0, 10, 0, 12)},
    "2x4":{"fraction" : (2,4), "symbol" : ("\uE082","\uE084"), "size":40, "margins": (0, 10, 0, 12)},
    "3x2":{"fraction" : (3,2), "symbol" : ("\uE083","\uE082"), "size":40, "margins": (0, 10, 0, 12)},
    "3x4":{"fraction" : (3,4), "symbol" : ("\uE083","\uE084"), "size":40, "margins": (0, 10, 0, 12)},
    "4x4":{"fraction" : (4,4), "symbol" : ("\uE084","\uE084"), "size":40, "margins": (0, 10, 0, 12)},
    "6x8":{"fraction" : (6,8), "symbol" : ("\uE086","\uE088"), "size":40, "margins": (0, 10, 0, 12)},
    "9x8":{"fraction" : (9,8), "symbol" : ("\uE089","\uE088"), "size":40, "margins": (0, 10, 0, 12)},
    "12x8":{"fraction" : (12,8), "symbol" : ("\uE082","\uE088"), "size":40, "margins": (0, 10, 0, 12)}
}

# because the clef is centered around the top of the staff, we want to push it down based on where it's center is
supported_clef_settings = {
    TREBLE_CLEF : { # for treble, center is around the center of the circle
        "size" : 44,
        "font_code": "\uE050",
        "margins":(20,44,0,10),
        "notes_per_line":["E4","G4","B4","D5","F5"], # this depends on key signature.
        "notes_per_interval":["F4","A4","C5","E5"],
        "signature_position_pattern": {
            "C": [],
            "G": [{"F":(0,1)}],
            "D": [{"F":(0,1)}, {"C":(1,2)}],
            "A": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}],
            "E": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}],
            "B": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}, {"A":(1,3)}],
            "F#": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}, {"A":(1,3)}, {"E":(1,1,"F")}],
            "C#": [{"F":(0,1)}, {"C":(1,2)}, {"G":(1,-1)}, {"D":(0,2)}, {"A":(1,3)}, {"E":(1,1,"F")},{"B":(0,3,"C")}],
            "F":  [{"B":(0,3)}],
            "Bb":  [{"B":(0,3)},{"E":(1,1)}],
            "Eb":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)}],
            "Ab":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)}],
            "Db":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)},{"G":(0,4)}],
            "Gb":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)},{"G":(0,4)},{"C":(1,2,"B")}],
            "Cb":  [{"B":(0,3)},{"E":(1,1)}, {"A":(1,3)},{"D":(0,2)},{"G":(0,4)},{"C":(1,2,"B")},{"F":(1,4,"E")}]
        }
    },
    BASS_CLEF : {  # for bass, center is around the big dot
        "size" : 40,
        "font_code": "\uE062",
        "margins":(18,11,0,0),
        "notes_per_line":("G2","B2","D3","F3","A3"),
        "notes_per_interval":("A2","C3","E3","G3"),
        "signature_position_pattern": {
            "C": [],
            "G": [{"F":(0,2)}], # 0 is for line, 1 is interval. in this case (0,2) => (line, index 2) 
            "D": [{"F":(0,2)}, {"C":(1,3)}], # (1,3) means 3rd interval
            "A": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}],
            "E": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}],
            "B": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}, {"A":(1,4)}],
            "F#": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}, {"A":(1,4)}, {"E":(1,2)}],
            "C#": [{"F":(0,2)}, {"C":(1,3)}, {"G":(1,1)}, {"D":(0,3)}, {"A":(1,4)}, {"E":(1,2)},{"B":(0,4)}],
            "F":  [{"B":(0,4)}],
            "Bb":  [{"B":(0,4)},{"E":(1,2)}],
            "Eb":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)}],
            "Ab":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)}],
            "Db":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)},{"G":(0,5)}],
            "Gb":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)},{"G":(0,5)},{"C":(1,3,"B")}],
            "Cb":  [{"B":(0,4)},{"E":(1,2)}, {"A":(1,4)},{"D":(0,3)},{"G":(0,5)},{"C":(1,3,"B")},{"F":(1,5,"E")}]
        }
    }
}

supported_modulations = {
    "MODULATION_SHARP": {
        "font_code": "\uE262",
        "key_signatures": ("C", "G", "D", "A", "E", "B", "F#", "C#"),
        "font_size": 40
    },
    "MODULATION_FLAT": {
        "font_code": "\uE260",
        "key_signatures": ("F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"),
        "font_size": 40
    }
}

lowest_note_code = 21 # midi number for lowest A note (first note on the left of 88-keys piano)
middle_c_code = 60 # midi note number for middle C 'C4'. index = 39

piano_notes_sharps = ['A0', 'A0#', 'B0', 'C1', 'C1#', 'D1', 'D1#', 'E1', 'F1', 'F1#', 'G1', 'G1#',
               'A1', 'A1#', 'B1', 'C2', 'C2#', 'D2', 'D2#', 'E2', 'F2', 'F2#', 'G2', 'G2#',
               'A2', 'A2#', 'B2', 'C3', 'C3#', 'D3', 'D3#', 'E3', 'F3', 'F3#', 'G3', 'G3#',
               'A3', 'A3#', 'B3', 'C4', 'C4#', 'D4', 'D4#', 'E4', 'F4', 'F4#', 'G4', 'G4#',
               'A4', 'A4#', 'B4', 'C5', 'C5#', 'D5', 'D5#', 'E5', 'F5', 'F5#', 'G5', 'G5#',
               'A5', 'A5#', 'B5', 'C6', 'C6#', 'D6', 'D6#', 'E6', 'F6', 'F6#', 'G6', 'G6#',
               'A6', 'A6#', 'B6', 'C7', 'C7#', 'D7', 'D7#', 'E7', 'F7', 'F7#', 'G7', 'G7#',
               'A7', 'A7#', 'B7', 'C8']

piano_notes_flats = [
    "A0", "B0b", "B0",
    "C1", "D1b", "D1", "E1b", "E1", "F1", "G1b", "G1", "A1b", "A1", "B1b", "B1",
    "C2", "D2b", "D2", "E2b", "E2", "F2", "G2b", "G2", "A2b", "A2", "B2b", "B2",
    "C3", "D3b", "D3", "E3b", "E3", "F3", "G3b", "G3", "A3b", "A3", "B3b", "B3",
    "C4", "D4b", "D4", "E4b", "E4", "F4", "G4b", "G4", "A4b", "A4", "B4b", "B4",
    "C5", "D5b", "D5", "E5b", "E5", "F5", "G5b", "G5", "A5b", "A5", "B5b", "B5",
    "C6", "D6b", "D6", "E6b", "E6", "F6", "G6b", "G6", "A6b", "A6", "B6b", "B6",
    "C7", "D7b", "D7", "E7b", "E7", "F7", "G7b", "G7", "A7b", "A7", "B7b", "B7",
    "C8"
]

piano_notes_key_patterns = {
    MODULATION_SHARP: {
        "C": [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27, 29, 31, 32, 34, 36, 38, 39, 41, 43, 44, 46, 48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 86, 87],
        "G": [0, 2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 27, 29, 31, 33, 34, 36, 38, 39, 41, 43, 45, 46, 48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72, 74, 75, 77, 79, 81, 82, 84, 86, 87],
        "D": [0, 2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86],
        "A": [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86],
        "E": [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26, 28, 30, 31, 33, 35, 36, 38, 40, 42, 43, 45, 47, 48, 50, 52, 54, 55, 57, 59, 60, 62, 64, 66, 67, 69, 71, 72, 74, 76, 78, 79, 81, 83, 84, 86],
        "B": [1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 18, 19, 21, 23, 25, 26, 28, 30, 31, 33, 35, 37, 38, 40, 42, 43, 45, 47, 49, 50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86],
        "F#": [1, 2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20, 21, 23, 25, 26, 28, 30, 32, 33, 35, 37, 38, 40, 42, 44, 45, 47, 49, 50, 52, 54, 56, 57, 59, 61, 62, 64, 66, 68, 69, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86],
        "C#": [1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30, 32, 33, 35, 37, 39, 40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76, 78, 80, 81, 83, 85, 87]
    },
    MODULATION_FLAT: {
        "F":  [0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20, 22, 24, 25, 27, 29, 31, 32, 34, 36, 37, 39, 41, 43, 44, 46, 48, 49, 51, 53, 55, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75, 77, 79, 80, 82, 84, 85, 87],
        "Bb": [0, 1, 3, 5, 6, 8, 10, 12, 13, 15, 17, 18, 20, 22, 24, 25, 27, 29, 30, 32, 34, 36, 37, 39, 41, 42, 44, 46, 48, 49, 51, 53, 54, 56, 58, 60, 61, 63, 65, 66, 68, 70, 72, 73, 75, 77, 78, 80, 82, 84, 85, 87],
        "Eb": [1, 3, 5, 6, 8, 10, 11, 13, 15, 17, 18, 20, 22, 23, 25, 27, 29, 30, 32, 34, 35, 37, 39, 41, 42, 44, 46, 47, 49, 51, 53, 54, 56, 58, 59, 61, 63, 65, 66, 68, 70, 71, 73, 75, 77, 78, 80, 82, 83, 85, 87],
        "Ab": [1, 3, 4, 6, 8, 10, 11, 13, 15, 16, 18, 20, 22, 23, 25, 27, 28, 30, 32, 34, 35, 37, 39, 40, 42, 44, 46, 47, 49, 51, 52, 54, 56, 58, 59, 61, 63, 64, 66, 68, 70, 71, 73, 75, 76, 78, 80, 82, 83, 85, 87],
        "Db": [1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30, 32, 33, 35, 37, 39, 40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76, 78, 80, 81, 83, 85, 87],
        "Gb": [1, 2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20, 21, 23, 25, 26, 28, 30, 32, 33, 35, 37, 38, 40, 42, 44, 45, 47, 49, 50, 52, 54, 56, 57, 59, 61, 62, 64, 66, 68, 69, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86],
        "Cb": [1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 18, 19, 21, 23, 25, 26, 28, 30, 31, 33, 35, 37, 38, 40, 42, 43, 45, 47, 49, 50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81, 83, 85, 86]
    }
}

white_labels= ['A0', 'B0', 'C1', 'D1', 'E1', 'F1', 'G1',
               'A1', 'B1', 'C2', 'D2', 'E2', 'F2', 'G2',
               'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3',
               'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
               'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5',
               'A5', 'B5', 'C6', 'D6', 'E6', 'F6', 'G6',
               'A6', 'B6', 'C7', 'D7', 'E7', 'F7', 'G7',
               'A7', 'B7', 'C8']

black_labels = ['A0#', 'C1#', 'D1#', 'F1#', 'G1#',
                'A1#', 'C2#', 'D2#', 'F2#', 'G2#',
                'A2#', 'C3#', 'D3#', 'F3#', 'G3#',
                'A3#', 'C4#', 'D4#', 'F4#', 'G4#',
                'A4#', 'C5#', 'D5#', 'F5#', 'G5#',
                'A5#', 'C6#', 'D6#', 'F6#', 'G6#',
                'A6#', 'C7#', 'D7#', 'F7#', 'G7#',
                'A7#']

black_labels_flats = ['B0b', 'D1b', 'E1b', 'G1b', 'A1b',
                'B1b', 'D2b', 'E2b', 'G2b', 'A2b',
                'B2b', 'D3b', 'E3b', 'G3b', 'A3b',
                'B3b', 'D4b', 'E4b', 'G4b', 'A4b',
                'B4b', 'D5b', 'E5b', 'G5b', 'A5b',
                'B5b', 'D6b', 'E6b', 'G6b', 'A6b',
                'B6b', 'D7b', 'E7b', 'G7b', 'A7b',
                'B7b']