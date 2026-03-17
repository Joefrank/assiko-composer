
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
        self.parent:Control = parent
        self.children = []
        self.supported_events = []
        self.z_index = 0
        self.is_resizable = False
        self.grid_coordinates = None  # (row, col) if using grid layout. None means it's not placed in a grid
        self.grid_spacing = (0, 0)  # (horizontal_spacing, vertical_spacing)
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent
        parent.add_child(self)

    def get_children(self):
        return self.children
    
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
        for child in self.children:
            child.hide()