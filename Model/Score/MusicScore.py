import pygame

from DataClasses.Config.ScreenConfig import StaffConfig
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Model.Score.GrandStaff import GrandStaff
from Model.Score.Staff import Staff
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

        for staff in self.staves_sequence:
            staff.parent_container = container

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
        if self.parent_container is not None:
            staff.parent_container = self.parent_container

    def remove_staff(self, staff):
        if staff in self.staves_sequence:
            self.staves_sequence.remove(staff)

        staff_builder = self.get_child_item_builder("staff")
        if staff_builder and hasattr(staff_builder, "all_staves") and staff in staff_builder.all_staves:
            staff_builder.all_staves.remove(staff)

    def add_staff_after(self, staff):
        staff_builder = self.get_child_item_builder("staff")
        parent_page = getattr(staff, "parent_page", None)

        if staff_builder is None or parent_page is None:
            return None

        new_staff_top_left = (
            staff.rect.x,
            staff.rect.bottom + StaffConfig.STAFF_SPACING
        )
        new_staff = staff_builder.build_empty_staff(
            new_staff_top_left,
            StaffConfig.STAFF_WIDTH_PERCENT,
            parent_page
        )
        self.add_staff(new_staff)
        return new_staff

    def iter_staves(self):
        for staff_item in self.staves_sequence:
            if isinstance(staff_item, GrandStaff):
                for staff in staff_item.staves:
                    yield staff
            elif isinstance(staff_item, Staff):
                yield staff_item

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
        if self.renderer:
            self.renderer.render_score(self)
        if self.debug_on:
            self.draw_debug()

    def draw_debug(self):       
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

   
    """ This function is called when a symbol is dropped onto the score. It translates the drop coordinates to score space and creates a TextInput at that location."""
    def translate_coordinates_to_score_space(self, coordinates):
        if self.container_root_coordinates is None:
            return coordinates
        translated_x = coordinates[0] - self.container_root_coordinates[0]
        translated_y = coordinates[1] - self.container_root_coordinates[1]
        return (translated_x, translated_y)
    
    def CreateStaff(self, input_dict, rect):
        staff_builder = self.get_child_item_builder("staff")
        if staff_builder:
            parent_page = input_dict["parent_page"]
            new_staff = staff_builder.build_empty_staff((rect.x, rect.y), StaffConfig.STAFF_WIDTH_PERCENT, parent_page)
            self.add_staff(new_staff)
            return new_staff
        return None


    def CreateTextInput(self, input_dict, rect):        
        parent_page = input_dict["parent_page"]
        score_builder = self.get_child_item_builder("score")
        text_item =  score_builder.build_score_text_item(rect, parent_page=parent_page)
        parent_page.children.append(text_item)
        return text_item
    
    