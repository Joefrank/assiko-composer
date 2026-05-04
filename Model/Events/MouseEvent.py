
from DataClasses.Config.ScreenConfig import MouseEventType
from Model.Events.Event import Event
from Model.Geometry.Position import Position

class MouseEvent(Event):

    def __init__(self, event_type: MouseEventType):
        super().__init__()
        self.event_type = event_type
        self.previous_position = None
        self.current_position = None
       
    def get_previous_position(self):
        return self.previous_position
    
    def get_current_position(self):
        return self.current_position
    
    def set_previous_position(self, position: Position):
        self.previous_position = position

    def set_current_position(self, position: Position):
        self.previous_position = self.current_position
        self.current_position = position

    def notify(self) -> bool:
        if self.current_position is None:
            return False
        for listener in self.listeners:
            if self.event_type == MouseEventType.HOVER:
                listener.on_mouse_over(self.current_position)
            elif self.event_type == MouseEventType.CLICK:
                listener.on_mouse_left_click(self.current_position)
        return True

    def reset_current_position(self):
        self.previous_position = self.current_position
        self.current_position = None
        
    def reset(self):
        self.previous_position = None
        self.current_position = None

    
   

    
