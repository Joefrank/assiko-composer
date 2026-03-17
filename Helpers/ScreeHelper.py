
import pygame

from DataClasses.EventData import KEYBOARD_EVENTS, MOUSE_EVENTS


class ScreenHelper: 
    
    """Gets dimensions as ratio of current screen resolution."""
    @staticmethod 
    def get_dimensions_by_ratio(
        width_ratio=1.0, 
        height_ratio=1.0) -> tuple[int, int]: 
        info = pygame.display.Info()
        screen_width = int(info.current_w * width_ratio)
        screen_height = int(info.current_h * height_ratio)
        x = (info.current_w - screen_width) // 2
        y = (info.current_h - screen_height) // 2
        return screen_width, screen_height, x, y
    
    @staticmethod
    def is_mouse_event(event):        
        return event.type in MOUSE_EVENTS    
    
    @staticmethod
    def is_left_mouse_button_event(event):
        return (ScreenHelper.is_mouse_event(event) and hasattr(event, 'button') and event.button == 1)
    
    @staticmethod
    def is_keyboard_event(event):
        return event.type in KEYBOARD_EVENTS
    
    @staticmethod
    def create_font(font_spec):
        name, size = font_spec
        try:
            return pygame.font.Font(name, size)
        except Exception as e:
            return pygame.font.SysFont(name if isinstance(name, str) else None, size)