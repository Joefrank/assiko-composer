
"""
    This is represents a rectangular surface
"""
import pygame

from Model.Geometry.Position import Position


class Rect:
   
    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_left: Position = top_left
        self.top_right: Position = top_right
        self.bottom_right: Position = bottom_right
        self.bottom_left: Position = bottom_left

    def move(self, offset_x:int, offset_y:int):
        self.top_left.translateTo(offset_x, offset_y)
        self.top_right.translateTo(offset_x, offset_y)
        self.bottom_right.translateTo(offset_x, offset_y)
        self.bottom_left.translateTo(offset_x, offset_y)

    def move_y(self, offset_y:int):
        self.top_left.translate_y(offset_y)
        self.top_right.translate_y(offset_y)
        self.bottom_right.translate_y(offset_y)
        self.bottom_left.translate_y(offset_y)


    def get_rect(self):
        x = self.top_left.x
        y = self.top_left.y
        width = self.top_right.x - self.top_left.x
        height = self.bottom_left.y - self.top_left.y
        return x, y, width, height
    
    def __str__(self):
        return (f"Rectangle: top-left {self.top_left} - top-right{self.top_right} - bottom-right: {self.bottom_right} "
                f"- bottom-left: {self.bottom_left}")