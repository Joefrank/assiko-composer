
from enum import Enum

class TextPosition(Enum):
    CENTER = "center"
    TOP_CENTER = "top-center"
    BOTTOM_CENTER = "bottom-center"

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y