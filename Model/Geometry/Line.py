from Model.Geometry.Position import Position


class Line:

     def __init__(self, start_position, end_position, thickness, color, **kwargs):       
        super().__init__(**kwargs)
        self.start_position = start_position
        self.end_position = end_position
        self.thickness = thickness
        self.color = color

     def contains_position(self, position):
        return ((self.start_position.x <= position.x <= self.end_position.x and position.y == self.start_position.y)
        or (self.start_position.y <= position.y <= self.end_position.y and position.x == self.start_position.x))

     def is_above_position(self, position):
        return self.start_position.y < position.y and self.end_position.y < position.y
    
     def is_below_position(self, position):
        return self.start_position.y > position.y and self.end_position.y > position.y

     def translateTo(self, x:int, y:int):
        self.start_position.translateTo(x, y)
        self.end_position.translateTo(x, y)
        
     def moveTo(self, start_position: Position, end_position: Position):
        self.start_position = start_position
        self.end_position = end_position

     def __str__(self):
        return f"Straight Line - start: {self.start_position} - end: {self.end_position}"