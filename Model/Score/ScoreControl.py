

from Model.Control import Control


class ScoreControl(Control):

    def __init__(self, rect, control_type, name, parent):
        super().__init__(rect, control_type=control_type, name=name, parent=parent) 

    def move(self, offset_x:int, offset_y:int):
        self.rect.x += offset_x
        self.rect.y += offset_y

    def move_y(self, offset_y:int):
        self.rect.y += offset_y

    def unlink(self, control):
        self.children.remove(control)
        
    """Score control can be deleted. All references should be set to null."""
    def delete(self):
        self.parent.unlink(self)
        self.parent = None
        
        if not self.children or len(self.children) == 0:
            return
        
        for child in self.children:           
            child.delete()
