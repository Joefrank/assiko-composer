

from DataClasses.ControlData import ControlType
from Model.Control import Control


class ButtonSymbol(Control):

    def __init__(self, label, rect, name):
        super().__init__(rect, ControlType.STAGGERED_BUTTON_SYMBOL, name)
        self.label = label # Full label with font

    def move_horizontally(self, x_offset):
        self.rect.x += x_offset

    def move_vertically(self, y_offset):
        self.rect.y += y_offset

    def move(self, h_move, v_move):
        self.move_horizontally(h_move)
        self.move_vertically(v_move)

 