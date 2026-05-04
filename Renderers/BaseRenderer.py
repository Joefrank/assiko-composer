import pygame

from collections import defaultdict
from DataClasses.Config import ScreenConfig
from DataClasses.Config.MusicConfig import NoteDurationInTicks, NoteOptions, default_note_duration
from DataClasses.Config.ScreenConfig import Color, StaffConfig
from Helpers.ScreeHelper import ScreenHelper
from Model.Geometry.Position import Position
from Model.Score.Note import Note

class BaseRenderer:

    @property
    def screen(self):
        return self.state.screen
    
    def __init__(self, state):
        self.state = state
        self.screen_init_time = None
        self.original_screen = None
        self.active_screen = None       
        # put these in config
        self.default_note_duration = default_note_duration

    @property
    def screen(self):
        return self.active_screen if self.active_screen is not None else self.state.screen

    def render_mouse_tracker(self, position, key_id):
        note_duration = self.get_registered_note_duration()
        self.draw_note(note_duration, key_id, 40, 30, position) 

    def draw_rect_surface(self, width, height, surface_color, alpha, position):
        if self.original_screen is None:
            print("Screen has not been initialized.")
            return
        # Create a temporary surface with per-pixel alpha
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill with background color but apply transparency
        rect_surface.fill((*surface_color, alpha))  # RGBA
        # Draw the transparent rectangle at (100, 100)
        self.original_screen.blit(rect_surface, (position.x, position.y))

    """ 
        Draws text on screen. position: Position object
    """
    def draw_text(self, screen, text, position, font_size, container_width=100, font_color=(0, 0, 0), text_alignment="LEFT"):
        font = pygame.font.SysFont(None, font_size)  # None = default font, 48 = font size
        
        try:
            text_renderer = font.render(text, True, font_color)
        except Exception as e:
            print(f"Error rendering text '{text}': {e}")
           
        if text_alignment == "RIGHT":
            text_rect = text_renderer.get_rect()
            text_rect.topright = (position.x, position.y) # 20 px for padding
            screen.blit(text_renderer, text_rect)
        elif text_alignment == "CENTER": # position here is the will be x: staff_top_left and y where you want title
            text_block_x = (container_width // 2) - (text_renderer.get_width() // 2)
            screen.blit(text_renderer, (position.x + text_block_x, position.y))
        else:
            screen.blit(text_renderer, (position.x, position.y))  # White color text

    def draw_line_from_point(self, start_point, end_point, color=(0, 0, 0), thickness=1):
        pygame.draw.line(self.screen, color, (start_point.x, start_point.y),
                         (end_point.x, end_point.y), thickness)
        
    def draw_line(self, line, color=(0, 0, 0), thickness=1):
        self.draw_line_from_point(line.start_position, line.end_position, color, 
                                  thickness if line.thickness is None else line.thickness) 

    """ 
        note_type: duration of note (1: note, 2: semi-brev , 4:quaver), 
        note_size: font-size, 
        position: bottom-left position
    """
    def draw_note(self, note_duration_details, note_name, note_size, stem_height, position, color=(100, 100, 100)):
        note_font_size = ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, note_size))
        note = note_font_size.render(note_duration_details[2], True, color)
        # Get its rect and move it
        note_rect = note.get_rect(center=position.get_tuple())
        self.screen.blit(note, note_rect)

        # draw stem only if config says so
        if note_duration_details[3]:
            stem_start = (note_rect.right - 2, position.y)  # stem on right
            stem_end = (note_rect.right - 2, position.y - stem_height)
            pygame.draw.line(self.screen, color, stem_start, stem_end, 2) 

        text_position = Position(position.x + 5, position.y)           
        self.draw_text(self.screen, note_name, text_position, 20, font_color=color)

    def render_symbol(self, size, symbol_value, position, color=Color.BLACK):
        font = ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, size))
        surface = font.render(symbol_value, True, color)
        note_rect = surface.get_rect(center=position.get_tuple())
        self.screen.blit(surface, note_rect)
        return note_rect

    def render_note_head(self, note:Note, note_color=Color.BLACK) -> None:        
        # render main note symbol       
        self.render_symbol(StaffConfig.STAFF_NOTE_SIZE, note.get_head_font_code(), note.position, note_color)

        # check for extention - staccato
        if note.staccato:
            staccato_offset = note.position.y - 7 if note.stem_inverted else note.position.y + 10
            stacc_position = Position(note.position.x, staccato_offset)
            self.render_symbol(StaffConfig.STACCATO_SYMBOL_SIZE, NoteOptions.STACCATO, stacc_position, note_color)
        
        # check note extension
        if note.extended:
            extended_position = Position(note.position.x + 12, note.position.y)
            self.render_symbol(StaffConfig.STACCATO_SYMBOL_SIZE, NoteOptions.STACCATO, extended_position, note_color)

    def render_note(self, note:Note, show_key_id:bool =False, note_color=Color.BLACK, 
                    text_color=Color.BLACK) -> None:
       
        # render main note symbol
        note_rect = self.render_symbol(StaffConfig.STAFF_NOTE_SIZE, note.duration[2], note.position, note_color)
        # check for extention - staccato
        if note.staccato:
            staccato_offset = note.position.y - 7 if note.stem_inverted else note.position.y + 10
            stacc_position = Position(note.position.x, staccato_offset)
            self.render_symbol(StaffConfig.STACCATO_SYMBOL_SIZE, NoteOptions.STACCATO, stacc_position, note_color)
        
        # check note extension
        if note.extended:
            extended_position = Position(note.position.x + 12, note.position.y)
            self.render_symbol(StaffConfig.STACCATO_SYMBOL_SIZE, NoteOptions.STACCATO, extended_position, note_color)

        # draw stem only if config says so
        if note.duration[3]:
            # check note inversion
            line_end_y = note.position.y
            if note.stem_inverted:               
                line_end_y +=  StaffConfig.STAFF_NOTE_STEM_SIZE
            else:
                line_end_y -=  StaffConfig.STAFF_NOTE_STEM_SIZE

            extra_stem_x_offset = 2 if note.duration[4] > NoteDurationInTicks.QUARTER else 0 # adjust stem x position based on inversion
            stem_x_offset = note.position.x + ((-6 - extra_stem_x_offset) if note.stem_inverted else 4 + extra_stem_x_offset)
            stem_start = (stem_x_offset, note.position.y)  # stem on right
            stem_end = (stem_x_offset, line_end_y)
            pygame.draw.line(self.screen, note_color, stem_start, stem_end, 2) 

        # show accidentals if necessary
        if note.accidental is not None:
            accidental_position = Position(note.position.x - 12, note.position.y)
            self.render_symbol(StaffConfig.STAFF_ACCIDENTAL_SIZE, note.accidental[1], accidental_position, note_color)           

        # show the note name if necessary
        if show_key_id:
            text_position = Position(note.position.x + 10, note.position.y)           
            self.draw_text(self.screen, note.key_id, text_position, 20, font_color=text_color)

    def render_chord(self, chord_notes: list[Note], 
                     inverted:bool =False, show_chord_name:bool =False) -> None:      
        grouped = defaultdict(list)
        # group notes by their exact duration to handle same notes in chord
        for note in chord_notes:
            key = note.get_exact_duration()[0]  # 5th element (index 4)
            grouped[key].append(note)

        grouped = dict(grouped)  # optional
        processed_groups_count = 0

        for key, notes in grouped.items():
            inverted = inverted if processed_groups_count % 2 == 0 else not inverted
            # if we have only one note, let it displayed as usual
            if len(notes) == 1:
                note = notes[0]
                note.stem_inverted = inverted
                color = Color.BLACK if note.color is None else note.color
                self.render_note(note, True, color, color)               
                processed_groups_count += 1                
                continue
            elif len(notes) > 1:                        
                inverted = not inverted
                top_note = min(notes, key=lambda n: n.position.y)
                bottom_note = max(notes, key=lambda n: n.position.y)
                stem_height = abs(top_note.position.y - bottom_note.position.y) + (StaffConfig.STAFF_NOTE_STEM_SIZE * 0.75)
                stem_color = Color.BLACK if top_note.color is None else top_note.color
                print(f"Rendering chord with {len(notes)} notes - inverted: {inverted} - stem height: {stem_height}")
                for note in notes:
                    self.render_note_head(note, note.color if note.color is not None else Color.BLACK)

                #if not has stem by default then we will draw the connecting step
                if notes[0].duration[3] == True \
                    or (notes[0].duration[3] == False and note.duration[4] <= NoteDurationInTicks.QUARTER):
                    extra_stem_x_offset = 2 if key > NoteDurationInTicks.QUARTER else 0 # adjust stem x position based on inversion
                    stem_x_offset = top_note.position.x + ((-6 - extra_stem_x_offset) if inverted else 4 + extra_stem_x_offset)  # adjust stem x position based on inversion
                    stem_start = Position(stem_x_offset, top_note.position.y) if inverted \
                        else Position(stem_x_offset, bottom_note.position.y)
                    stem_end = Position(stem_x_offset, top_note.position.y + stem_height) if inverted \
                        else Position(stem_x_offset, bottom_note.position.y - stem_height)
                    pygame.draw.line(self.screen, stem_color, stem_start.get_tuple(), stem_end.get_tuple(), 2)
                
                if note.duration[4] <= NoteDurationInTicks.QUARTER: # these notes have flags/beams
                    # draw beams/flags between notes
                    number_of_flags = 0
                    match key:
                        case NoteDurationInTicks.EIGHT:
                            number_of_flags = 1
                        case NoteDurationInTicks.SIXTHEENTH:
                            number_of_flags = 2
                        case _:
                            number_of_flags = 0
                    
                    beam_spacing = 6
                    
                    for i in range(number_of_flags):
                        beam_y_offset = beam_spacing * (i + 1)
                        beam_start = (stem_x_offset - 3, stem_end.y + beam_y_offset if inverted else stem_end.y - beam_y_offset)
                        beam_end = (stem_x_offset + 10, stem_end.y + beam_y_offset if inverted else stem_end.y - beam_y_offset)
                        pygame.draw.line(self.screen, stem_color, beam_start, beam_end, 4)

                processed_groups_count += 1
            
     

    def draw_rect_surface(self, screen, width, height, surface_color, alpha, position):  
        # Create a temporary surface with per-pixel alpha
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill with background color but apply transparency
        rect_surface.fill((*surface_color, alpha))  # RGBA
        # Draw the transparent rectangle at (100, 100)
        screen.blit(rect_surface, (position.x, position.y))

    def get_registered_note_duration(self):
         note_duration = self.state.get_registered_key() 
         if note_duration is None:
            note_duration = self.default_note_duration 
         return note_duration