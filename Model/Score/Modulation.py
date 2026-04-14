
from Model.Geometry.Position import Position


class Modulation:  

    def __init__(self, key, position: Position, staff_item):
        self.key = key
        self.position = position
        self.staff_item = staff_item