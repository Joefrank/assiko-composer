
from enum import Enum

class TextPosition(Enum):
    CENTER = "center"
    TOP_CENTER = "top-center"
    BOTTOM_CENTER = "bottom-center"

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    """
        Compares this point with another to see if they are the same.
    """
    def is_same_as(self, position):
        return position.x == self.x and position.y == self.y
    
    """ 
        Determines if this position is on a horizontal or vertical line.
        This works for straight lines only. which is what we use on a staff.
    """
    def is_on_line(self, line):
        return (
            (line.start_position.x == self.x and line.end_position.x == line.start_position.x)
            or line.start_position.y == self.y and line.start_position.y == line.end_position.y)
    
    """
        Determines if a given position lies within a rectangle.
    """
    def is_within_rectangle(self, rectangle):
        return(
            (rectangle.top_left.x <= self.x <= rectangle.top_right.x)
            and (rectangle.top_left.y <= self.y <= rectangle.bottom_right.y)
        )
    
    """
        Determines if a given position belongs to a specific interval.
    """
    def belongs_to_interval(self, interval):
        return self.is_within_rectangle(interval.position_rect)

    def from_tuple(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        
    def get_tuple(self):
        return (self.x, self.y)
    
    def copy(self, other_position):
        self.x = other_position.x
        self.y = other_position.y

    def translateTo(self, position):
        self.x += position.x
        self.y += position.y

    def translateTo(self, x, y):
        self.x += x
        self.y += y

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def moveHorizontallyTo(self, x):
        self.x = x  

    def moveVerticallyTo(self, y):
        self.y = y
        
    def is_above_position(self, position):
        return self.y < position.y
    
    def is_below_position(self, position):
        return self.y > position.y
    
    def __str__(self):
        return f"Position:({self.x},{self.y})"