import os
import sys
import pygame
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Model.Score.GrandStaff import GrandStaff
from Model.Score.Staff import Staff
from Model.Score.ScoreControl import ScoreControl


class DummyRect:
    def __init__(self, x=0, y=0, width=100, height=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.topleft = (x, y)
        self.bottomright = (x + width, y + height)
        self.bottomleft = (x, y + height)
        self.topright = (x + width, y)
        self.top = y
        self.bottom = y + height


class DummyParent:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 400, 800)
        self.scroll_y = 0
        self.children = []
        self.app_state = None

    def unlink(self, control):
        if control in self.children:
            self.children.remove(control)

    def map_coordinates_in_viewport(self, coordinates):
        return coordinates


class DummyStaff:
    def __init__(self, name):
        self.name = name
        self.rect = pygame.Rect(0, 0, 100, 20)
        self.children = []
        self.parent = None
        self.app_state = None
        self.supported_events = []
        self.visible = True
        self.top_left_position = (0, 0)
        self.bottom_right_position = (100, 20)
        self.bottom_left_position = (0, 20)
        self.top_right_position = (100, 0)
        self.last_opened_dialog = None

    def move(self, offset_x, offset_y):
        self.rect.x += offset_x
        self.rect.y += offset_y

    def delete(self):
        if self.parent is not None:
            self.parent.unlink(self)
            self.parent = None

    def unlink(self, control):
        if control in self.children:
            self.children.remove(control)


class GrandStaffDeleteTests(unittest.TestCase):
    def test_delete_removes_all_child_staves_without_error(self):
        parent = DummyParent()
        staff1 = DummyStaff("staff1")
        staff2 = DummyStaff("staff2")
        grand_staff = GrandStaff(DummyRect(), "grand", [staff1, staff2], parent)
        grand_staff.parent = parent
        grand_staff.app_state = None
        grand_staff.children = [staff1, staff2]
        grand_staff.staves = [staff1, staff2]

        grand_staff.delete()

        self.assertEqual(grand_staff.children, [])
        self.assertEqual(grand_staff.staves, [])


if __name__ == "__main__":
    unittest.main()
