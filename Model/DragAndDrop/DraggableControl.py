# -----------------------------
# Draggable Symbol
# -----------------------------
import pygame


class DraggableControl:
    def __init__(self, rect):      
        self.rect = rect
        self.dragging = False
        self.offset = (0, 0)
        self.translate_coordinates_function = None
   
    def set_translate_coordinates_function(self, func):
        self.translate_coordinates_function = func

    def on_left_mouse_down(self, event): 
        position = self.translate_coordinates_function(event.pos) if self.translate_coordinates_function else event.pos      
        if self.rect.collidepoint(position):
           # print(f"on_left_mouse_down called with event at {event.pos}")
            self.dragging = True                
            # offset keeps the cursor from snapping to top-left
            self.offset = (
                self.rect.x - event.pos[0],
                self.rect.y - event.pos[1]
            )
    
    def on_left_mouse_up(self, event): 
        self.dragging = False

    def on_mouse_motion(self, event):
        if self.dragging:
            self.rect.x = event.pos[0] + self.offset[0]
            self.rect.y = event.pos[1] + self.offset[1]