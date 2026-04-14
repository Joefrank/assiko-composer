

"""
    This is represents a rectangular surface
"""
from Model.Geometry.Position import Position


class IntervalRect:
   
    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_left: Position = top_left
        self.top_right: Position = top_right
        self.bottom_right: Position = bottom_right
        self.bottom_left: Position = bottom_left

    def __str__(self):
        return (f"Rectangle: top-left {self.top_left} - top-right{self.top_right} - bottom-right: {self.bottom_right} "
                f"- bottom-left: {self.bottom_left}")