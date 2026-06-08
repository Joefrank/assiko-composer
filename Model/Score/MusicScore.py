import pygame

from DataClasses.Config.EventsConfig import TextInputBlinkTimer
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Model.Geometry import Position
from Model.Inputs.TextInput import TextInput
from Renderers import MusicScoreRenderer


class MusicScore:
    TICKS_PER_BEAT = 480
    
    def __init__(self, top_left, event_handler:MainWindowEventHandler, score_width=None, title=None, credits=None, tempo=80):        
        self.staves_sequence = [] #combination of all GrandStaves, could also be simple staffs         
        self.staff_color = None
        self.key_signature_list = None
        self.title_position = None
        self.highest_credit_y_offset = None
        self.credits = [] # array of text blocks to be added to the top of score apart from title.        
        self.lyrics = []
        self.top_left_position = top_left
        self.container_root_coordinates = None
        self.score_width = score_width
        self.title = title
        self.raw_credits = credits # these need processing    
        self.children_item_builders = {}
        self.renderer: MusicScoreRenderer = None
        self.app_state = None
        self.screen: pygame.Surface = None
        self.text_inputs = []
        self.window_event_handler = event_handler
        # sets debug mode for score.
        self.debug_on = True
        self.parent_container = None
       
      
    def set_parent_container(self, container):
        self.parent_container = container
        if self.parent_container.rect.width > self.score_width:
            x = (self.parent_container.rect.width - self.score_width) // 2
            self.top_left_position = (self.top_left_position[0] + x, self.top_left_position[1])

    def get_parent_container(self):
        return self.parent_container
    
    def contains_rect(self, rect):
        if self.container_root_coordinates is None:
            return False
        # Assuming a very large height for the score. We can extend the height dynamically.
        score_rect = pygame.Rect(0, 0, self.score_width, 10000)  
        return score_rect.colliderect(rect)
    
    def get_text_inputs(self):
        return self.text_inputs
    
    def set_root_coordinates(self, coordinates):
        self.container_root_coordinates = coordinates

    def get_root_coordinates(self):
        return self.container_root_coordinates
    
    def set_state(self, app_state):
        self.app_state = app_state

    def set_screen(self, screen: pygame.Surface):
        self.screen = screen
        
    def add_staff(self, staff):
        self.staves_sequence.append(staff)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left   

    def set_score_width(self, score_width):
        self.score_width = score_width

    def get_all_notes_in_positional_order(self):
        notes = []
        for staff in self.staves_sequence:
            notes.extend(staff.get_notes())
        return sorted(notes, key=lambda note: note.position.x)
    
    def find_nearest_staff_item_to_position(self, position):        
        for staff in self.staves_sequence:
            nearest_item = staff.find_nearest_item_to_position(position)
            if nearest_item is not None:
                return nearest_item
          
        return None  

    def add_child_item_builder(self, item_type, builder):
        self.children_item_builders[item_type] = builder

    def get_child_item_builder(self, item_type):
        return self.children_item_builders.get(item_type, None)
    
    def set_renderer(self, renderer):
        self.renderer = renderer

    def get_renderer(self):
        return self.renderer

    def draw(self):
        #if self.renderer:
            #self.renderer.render_score(self)
        if self.debug_on:
            self.draw_debug()

    def draw_debug(self):
        # Draw a border around the score for debugging
        #import traceback
        # print(f"draw_debug called - debug_on={self.debug_on}")
        #print("".join(traceback.format_stack()[-4:-1]))
        #self.debug_on = False  # Disable debug after drawing once to prevent clutter
        
        if self.screen and self.container_root_coordinates:
            _, scroll_y = self.parent_container.get_scroll_position()
            debug_rect = pygame.Rect(self.top_left_position[0], 
                                     self.top_left_position[1], self.score_width,
                                       self.parent_container.rect.height + scroll_y)  
            # Assuming a very large height for the score. We can extend the height dynamically.
           
            pygame.draw.rect(
                self.screen,
                (255, 100, 100),  # Red color for debug border
                debug_rect,
                2  # Border width
            )

    def CreateStaff(self, params_input, rect):
        staff_builder = self.get_child_item_builder("staff")
        if staff_builder:
            new_staff = staff_builder.build_empty_staff((rect.x, rect.y), self.score_width)
            self.staves_sequence.append(new_staff)
            return new_staff
        return None

    """ This function is called when a symbol is dropped onto the score. It translates the drop coordinates to score space and creates a TextInput at that location."""
    def translate_coordinates_to_score_space(self, coordinates):
        if self.container_root_coordinates is None:
            return coordinates
        translated_x = coordinates[0] - self.container_root_coordinates[0]
        translated_y = coordinates[1] - self.container_root_coordinates[1]
        return (translated_x, translated_y)
    
    def CreateTextInput(self, params_input, event_rect):
        real_coordinates = self.translate_coordinates_to_score_space((event_rect.x, event_rect.y))
        new_rect = pygame.Rect(real_coordinates[0], real_coordinates[1], 200, 40)
        text_input = TextInput(self.screen, self, new_rect, font_size=30)
        self.window_event_handler.subscribe(pygame.MOUSEBUTTONDOWN, text_input)
        self.window_event_handler.subscribe(pygame.KEYDOWN, text_input)
        self.window_event_handler.subscribe_timer(TextInputBlinkTimer.NAME, text_input)
        self.text_inputs.append(text_input)
        