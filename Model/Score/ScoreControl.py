

from Model.Control import Control


class ScoreControl(Control):

    def __init__(self, rect, control_type, name, parent):
        super().__init__(rect, control_type=control_type, name=name, parent=parent) 

    def move(self, offset_x:int, offset_y:int):
        self.rect.x += offset_x
        self.rect.y += offset_y