
import pygame

from DataClasses.ControlData import ControlType

class Control:
    HAND_CURSOR = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    ARROW_CURSOR = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)  

    def __init__(self, rect, control_type:ControlType, name, parent=None):
        self.Id = id(self)
        self.type:ControlType = control_type
        self.name = name
        self.rect= rect
        self.position = (rect.x, rect.y)  # (x, y)
        self.size = (rect.width, rect.height)          # (width, height)
        self.visible = True
        self.__parent:Control = parent
        self.children = []
        self.supported_events = []
        self.z_index = 0
        self.is_resizable = False
        self.grid_coordinates = None  # (row, col) if using grid layout. None means it's not placed in a grid
        self.grid_spacing = (0, 0)  # (horizontal_spacing, vertical_spacing)
        self.app_state = None        
        

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):        
        self.__parent = value

    @property
    def main_window(self):
        return self.app_state.get_main_window()
    
    @property
    def main_window_event_handler(self):
        return self.main_window.get_event_handler()

    @property
    def translator(self):
        return self.app_state.translator
    
    """Counts the number of children controls of specific type."""
    @staticmethod
    def number_children_of_type(parent, control_type:ControlType):
        return sum(1 for child in parent.children if child.type == control_type)

    def translate(self, key, language=None):
        if self.translator is None:
            return key  # No translator set, return the key as is
        return self.translator.t(key, language)
    
    def get_app_state(self):
        return self.app_state
    
    def set_app_state(self, app_state):
        # State doesn't get ovewritten but modified.
        if self.app_state is None:
            self.app_state = app_state
        
        if len(self.children) > 0:
            for child in self.children:
                child.set_app_state(app_state) 

    def reset_app_state(self):
        if len(self.children) > 0:
            for child in self.children:
                child.set_app_state(self.app_state) 

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_children(self, children):
        self.children += children
        
    def set_parent(self, parent):
        self.parent = parent
        if not self in parent.children:
            parent.add_child(self)

    def get_children(self):
        return self.children

    def get_children_of_type(self, control_type:ControlType):
        if len(self.children) == 0:
            return []
        
        return [child for child in self.children if child.type ==control_type]

    def get_children_of_instance(self, target_type):
        if len(self.children) == 0:
            return []
        
        return [child for child in self.children if isinstance(child, target_type)]

    def get_parent(self):
        return self.parent
    
    def set_z_index(self, z_index):
        self.z_index = z_index
        
    def add_supported_event(self, event_type):
        self.supported_events.append(event_type)

    def add_supported_events(self, event_types):
        self.supported_events.extend(event_types)

    def is_mouse_over(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def resize_only(self, new_width_ratio, new_height_ratio):
        if not self.is_resizable:
            return
        self.rect.width = int(self.rect.width * new_width_ratio)
        self.rect.height = int(self.rect.height * new_height_ratio)
        self.size = (self.rect.width, self.rect.height)

    def reset_position(self, new_width_ratio, new_height_ratio):
        self.rect.x = int(self.rect.x * new_width_ratio)
        self.rect.y = int(self.rect.y * new_height_ratio)
        self.position = (self.rect.x, self.rect.y)

    def resize(self, new_width_ratio, new_height_ratio):
        self.resize_only(new_width_ratio, new_height_ratio)        
        children_sizes = self.resize_children(new_width_ratio, new_height_ratio)      
        return self.size, children_sizes

    def resize_children(self, new_width_ratio, new_height_ratio):
        # resize and return new size of children controls if they are resizable
        children_sizes = {}
        for child in self.children:
            child.resize(new_width_ratio, new_height_ratio)
            children_sizes[child.name] = child.size
        return children_sizes
    
    def draw(self):
        # base control doesn't have a visual representation, it's just a container for other controls, so we don't draw anything here
        if not self.visible:
            return
        
    def hide(self):
        self.visible = False
        if len(self.children) == 0:
            return
        for child in self.children:
            child.hide()

    def show(self):
        self.visible = True
        if len(self.children) == 0:
            return
        for child in self.children:
            child.show()