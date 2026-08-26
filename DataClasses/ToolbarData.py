from dataclasses import dataclass

import pygame

from DataClasses.ButtonData import ButtonType
from DataClasses.Config import ScreenConfig
from DataClasses.Config.MusicConfig import BASS_CLEF, TREBLE_CLEF, AccidentalOptions, NoteDurationInTicks
from DataClasses.ControlData import ControlType
from Model.Buttons.ButtonIcon import ButtonIcon
from Model.Geometry.Position import TextPosition

@dataclass
class ToolbarDimensions:
    BUTTON_WIDTH = 40
    BUTTON_HEIGHT = 30
    BUTTON_MARGIN = 5
    BUTTON_BORDER_RADIUS = 6
    TOP_OFFSET_RATIO = 0.1
    TOOLBAR_HEIGHT_RATIO = 0.06
    TOOLBAR_ITEM_HEIGHT_RATIO = 0.038
    TOOLBAR_ITEM_WIDTH_RATIO = 0.025
    DEFAULT_TOOLBAR_WIDTH = 10
    TOOLBAR_SPACING = 20

@dataclass
class BaseToolbar:
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (25, 25, 25)
    BUTTON_BG_COLOR = (255, 200, 200)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (200, 180, 180)
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.CENTER
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 18)
    DRAGGABLE_BUTTONS = True # TODO: rename to draggable_symbols, as it makes more sense
    SUPPORTED_EVENTS = [pygame.MOUSEMOTION]
    BUTTON_TYPE = ButtonType.BUTTON

@dataclass
class PlayToolbar(BaseToolbar):
    NAME = "PlayToolbar"
    ICONS = [  
        ButtonIcon(symbol="⏮", tooltip_key="PreviousScore", name="Previous Score", action="Previous_Score"),
        ButtonIcon(symbol="▶", tooltip_key="PlayScore", name="Play Score", action="Play_Score"),
        ButtonIcon(symbol="⏸", tooltip_key="PauseScore", name="Pause Score", action="Pause_Score"),
        ButtonIcon(symbol="⏹", tooltip_key="StopScore", name="Stop Score", action="Stop_Score"),
        ButtonIcon(symbol="⏭", tooltip_key="NextScore", name="Next Score", action="Next_Score")
    ]
    FONT = (ScreenConfig.FontConfig.NOTO_SANS_SYMBOLS2_REGULAR, 14)
    DRAGGABLE_BUTTONS = False
    BG_COLOR = (220, 220, 220, 100)
    BG_HIGHLIGHT = (220, 220, 250)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    BUTTON_BG_COLOR = (70, 70, 70)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)
    BUTTON_HOVER_BG_COLOR = (100, 100, 100)

@dataclass
class NotesToolbar(BaseToolbar):
    NAME = "NotesDurationToolbar"
    ICONS =[
        ButtonIcon(symbol="\U0001D15D", tooltip_key="WholeNote", name="Whole Note", action_params={"duration": NoteDurationInTicks.WHOLE}),
        ButtonIcon(symbol="\U0001D15E", tooltip_key="HalfNote", name="Half Note", action_params={"duration": NoteDurationInTicks.HALF}),
        ButtonIcon(symbol="\U0001D15F", tooltip_key="QuarterNote", name="Quarter Note", action_params={"duration": NoteDurationInTicks.QUARTER}),
        ButtonIcon(symbol="\U0001D160", tooltip_key="EighthNote", name="Eighth Note", action_params={"duration": NoteDurationInTicks.EIGHT}),
        ButtonIcon(symbol="\U0001D161", tooltip_key="SixteenthNote", name="Sixteenth Note", action_params={"duration": NoteDurationInTicks.SIXTHEENTH}),
        ButtonIcon(symbol="\U0001D162", tooltip_key="ThirtySecondNote", name="Thirty-second Note", action_params={"duration": NoteDurationInTicks.THIRTYSECONDTH}),
        ButtonIcon(symbol="\U0001D163", tooltip_key="SixtyFourth", name="Sixty-fourth", action_params={"duration": NoteDurationInTicks.SIXTYFOURTH})
    ]   
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.BOTTOM_CENTER
    DROP_ACTION = "PositionNoteOnStaff"
 
@dataclass
class RestToolbar(BaseToolbar):
    NAME = "RestToolbar"
    ICONS =[
        ButtonIcon(symbol="\U0001D13B", tooltip_key="Whole", name="Whole", action_params={"duration": NoteDurationInTicks.WHOLE}),  # Whole
        ButtonIcon(symbol="\U0001D13C", tooltip_key="Half", name="Half", action_params={"duration": NoteDurationInTicks.HALF}),  # Half
        ButtonIcon(symbol="\U0001D13D", tooltip_key="Quarter", name="Quarter", action_params={"duration": NoteDurationInTicks.QUARTER}),  # Quarter
        ButtonIcon(symbol="\U0001D13E", tooltip_key="Eighth", name="Eighth", action_params={"duration": NoteDurationInTicks.EIGHT}),  # Eighth
        ButtonIcon(symbol="\U0001D13F", tooltip_key="Sixteenth", name="Sixteenth", action_params={"duration": NoteDurationInTicks.SIXTHEENTH}),  # Sixteenth
        ButtonIcon(symbol="\U0001D140", tooltip_key="ThirtySecond", name="32nd", action_params={"duration": NoteDurationInTicks.THIRTYSECONDTH}),  # 32nd
        ButtonIcon(symbol="\U0001D141", tooltip_key="SixtyFourth", name="64th", action_params={"duration": NoteDurationInTicks.SIXTYFOURTH}),  # 64th
        #ButtonIcon(symbol="\U0001D142", tooltip_key="OneTwentyEighth", name="128th", action_params={"duration": NoteDurationInTicks.ONE_TWENTY_EIGHTH}),  # 128th
    ]
    DROP_ACTION = "PositionRestOnStaff"

@dataclass
class AccidentalsToolbar(BaseToolbar):
    NAME: str = "AccidentalsToolbar"
    ICONS = [
        ButtonIcon(symbol="\uE262", tooltip_key="SHARPAccidental", name="SHARP Accidental", action_params={"accidental": AccidentalOptions.SHARP}),  # SHARP
        ButtonIcon(symbol="\uE260", tooltip_key="FLATAccidental", name="FLAT Accidental", action_params={"accidental": AccidentalOptions.FLAT}),  # FLAT
        ButtonIcon(symbol="\uE261", tooltip_key="NATURALAccidental", name="NATURAL Accidental", action_params={"accidental": AccidentalOptions.NATURAL}),   # NATURAL
        ButtonIcon(symbol="\uE263", tooltip_key="DOUBLE_SHARPAccidental", name="DOUBLE_SHARP Accidental", action_params={"accidental": AccidentalOptions.DOUBLE_SHARP}),   # DOUBLE_SHARP
        ButtonIcon(symbol="\uE264", tooltip_key="DOUBLE_FLATAccidental", name="DOUBLE_FLAT Accidental", action_params={"accidental": AccidentalOptions.DOUBLE_FLAT})   # DOUBLE_FLAT
    ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 25)
    DROP_ACTION = "PositionAccidental"

@dataclass
class TimeSignatureToolbar(BaseToolbar):
    NAME: str = "TimeSignatureToolbar"
    ICONS =[
                ButtonIcon(symbol=(chr(0xE082),chr(0xE082)), tooltip_key="Sign_2x2", name="Time:2x2", action_params={"time_signature": (2, 2)}),
                ButtonIcon(symbol=(chr(0xE082),chr(0xE084)), tooltip_key="Sign_2x4", name="Time:2x4", action_params={"time_signature": (2, 4)}),
                ButtonIcon(symbol=(chr(0xE083),chr(0xE082)), tooltip_key="Sign_3x2", name="Time:3x2", action_params={"time_signature": (3, 2)}),
                ButtonIcon(symbol=(chr(0xE083),chr(0xE084)), tooltip_key="Sign_3x4", name="Time:3x4", action_params={"time_signature": (3, 4)}),
                ButtonIcon(symbol=(chr(0xE084),chr(0xE084)), tooltip_key="Sign_4x4", name="Time:4x4", action_params={"time_signature": (4, 4)}),
                ButtonIcon(symbol=(chr(0xE086), chr(0xE088)), tooltip_key="Sign_6x8", name="Time:6x8", action_params={"time_signature": (6, 8)}),
                ButtonIcon(symbol=(chr(0xE089), chr(0xE088)), tooltip_key="Sign_9x8", name="Time:9x8", action_params={"time_signature": (9, 8)}),
                ButtonIcon(symbol=(chr(0xE081) + chr(0xE082), chr(0xE088)), tooltip_key="Sign_12x8", name="Time:12x8", action_params={"time_signature": (12, 8)})
            ]
    FONT = (ScreenConfig.FontConfig.BRAVURA_FONT_PATH, 18)   
    BUTTON_TEXT_CENTER: TextPosition = TextPosition.BOTTOM_CENTER   
    BUTTON_TYPE = ButtonType.TIME_SIGNATURE_BUTTON
    DROP_ACTION = "PositionTimeSignature"

@dataclass
class CommonTimeSignatureToolbar(BaseToolbar):
    NAME: str = "CommonTimeSignatureToolbar"
    ICONS =[
                ButtonIcon(symbol="\uE08A", tooltip_key="Common_Time", name="Time:4x4", action_params={"time_signature": (4, 4)}),
                ButtonIcon(symbol="\uE08B", tooltip_key="Cut_Time", name="Time:2x2", action_params={"time_signature": (2, 2)})                             
            ]
    DROP_ACTION = "PositionCommonTimeSignature"

@dataclass
class KeySignatureToolbar(BaseToolbar):
    NAME: str = "KeySignatureToolbar"
    ICONS =[
                ButtonIcon(symbol=("\uE262",1), tooltip_key="G_MAJOR", name="Key:G", action_params={"key_signature": "G"}),
                ButtonIcon(symbol=("\uE262",2), tooltip_key="D_MAJOR", name="Key:D", action_params={"key_signature": "D"}),
                ButtonIcon(symbol=("\uE262",3), tooltip_key="A_MAJOR", name="Key:A", action_params={"key_signature": "A"}),
                ButtonIcon(symbol=("\uE262",4), tooltip_key="E_MAJOR", name="Key:E", action_params={"key_signature": "E"}),
                ButtonIcon(symbol=("\uE262",5), tooltip_key="B_MAJOR", name="Key:B", action_params={"key_signature": "B"}),
                ButtonIcon(symbol=("\uE262",6), tooltip_key="F_SHARP_MAJOR", name="Key:F#", action_params={"key_signature": "F#"}),
                ButtonIcon(symbol=("\uE262",7), tooltip_key="C_SHARP_MAJOR", name="Key:C#", action_params={"key_signature": "C#"}),           
            ]
    BUTTON_TYPE = ButtonType.STAGGERED_SYMBOL_BUTTON
    DROP_ACTION = "PositionKeySignature"

@dataclass
class DynamicsToolbar(BaseToolbar):
    NAME: str = "DaynamicsToolbar"
    ICONS = [
        ButtonIcon(symbol="\uE52D", tooltip_key="Dyn_MF", name="mf", action_params={"dynamic": "mf"}),
        ButtonIcon(symbol="\uE52C", tooltip_key="Dyn_MP", name="mp", action_params={"dynamic": "mp"}),
        ButtonIcon(symbol="\uE522", tooltip_key="Dyn_F", name="f", action_params={"dynamic": "f"}),
        ButtonIcon(symbol="\uE520", tooltip_key="Dyn_P", name="p", action_params={"dynamic": "p"}),
        ButtonIcon(symbol="\uE52F", tooltip_key="Dyn_FF", name="ff", action_params={"dynamic": "ff"}),
        ButtonIcon(symbol="\uE52A", tooltip_key="Dyn_PP", name="pp", action_params={"dynamic": "pp"}),
        ButtonIcon(symbol="\uE530", tooltip_key="Dyn_FFF", name="fff", action_params={"dynamic": "fff"}),
        ButtonIcon(symbol="\uE52B", tooltip_key="Dyn_PPP", name="ppp", action_params={"dynamic": "ppp"}),
        ButtonIcon(symbol="\uE539", tooltip_key="Dyn_SFZ", name="sfz", action_params={"dynamic": "sfz"}),
        ButtonIcon(symbol="\uE537", tooltip_key="Dyn_SF", name="sf", action_params={"dynamic": "sf"}),
        ButtonIcon(symbol="\uE535", tooltip_key="Dyn_FZ", name="fz", action_params={"dynamic": "fz"}),
        ButtonIcon(symbol="\uE534", tooltip_key="Dyn_FP", name="fp", action_params={"dynamic": "fp"}),
        ButtonIcon(symbol="\uE536", tooltip_key="Dyn_RF", name="rf", action_params={"dynamic": "rf"}),
        ButtonIcon(symbol="\uE53E", tooltip_key="Dyn_CRESCENDO", name="crescendo", action_params={"dynamic": "crescendo"}),
        ButtonIcon(symbol="\uE53F", tooltip_key="Dyn_DIMINUENDO", name="diminuendo", action_params={"dynamic": "diminuendo"}),
    ]
    DROP_ACTION = "PositionDynamic"

@dataclass
class ClefToolbar(BaseToolbar):
    NAME: str = "ClefToolbar"
    ICONS =[
                ButtonIcon(symbol="\uE050", tooltip_key="Clef_TREBLE", name="treble_clef", action_params={"clef": TREBLE_CLEF}),
                ButtonIcon(symbol="\uE062", tooltip_key="Clef_BASS", name="bass_clef", action_params={"clef": BASS_CLEF})
            ]
    DROP_ACTION = "PositionClef"

@dataclass
class StaffActionToolbar(BaseToolbar):
    NAME: str = "StaffActionToolbar"
    ICONS = [
        ButtonIcon(symbol="music_staff.png", tooltip_key="Create_Staff_Key", name="create_staff", action="CreateStaff"),
        ButtonIcon(symbol="repeat_start.png", tooltip_key="Repeat_Start_Key", name="insert_start_repeat", action= "InsertStartRepeatToStaff"),
        ButtonIcon(symbol="repeat_end.png", tooltip_key="Repeat_End", name="insert_end_repeat", action= "InsertEndRepeatToStaff"),
        ButtonIcon(symbol="final_staff_line.png", tooltip_key="Final_Staff_Line", name="insert_final_staff_line", action= "InsertFinalStaffLine"),
        ButtonIcon(symbol="notes_tie.png", tooltip_key="Notes_Tie", name="tie_notes", action= "TieNotesOnStaff"),
        ButtonIcon(symbol="text.png", tooltip_key="Create_Text_Input_Key", name="create_text_input", action= "CreateTextInput"),
    ]
    BUTTON_TYPE = ButtonType.IMAGE_BUTTON 
    
TOOLBAR_MATRIX = [
    [NotesToolbar, AccidentalsToolbar, PlayToolbar, KeySignatureToolbar],
    [RestToolbar, TimeSignatureToolbar, CommonTimeSignatureToolbar, ClefToolbar, StaffActionToolbar]
]

@dataclass
class ToolbarGridConfig:
    GRID_SPACING = (5, 5)
    GRID_ROWS = 2
    GRID_COLS = 4
    GRID_NAME = "Horizontal_ToolbarGrid"