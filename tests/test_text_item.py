import os
import sys
import pygame
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Model.Inputs.TextItem import TextItem


class DummyContainer:
    def __init__(self):
        self.scroll_y = 0
        self.rect = pygame.Rect(0, 0, 400, 300)

    def get_drawing_boundaries(self):
        return 400, 0

    def map_coordinates_in_viewport(self, coordinates):
        return coordinates


class TextItemTests(unittest.TestCase):
    def test_draw_uses_text_based_cursor_position(self):
        pygame.init()
        pygame.font.init()

        container = DummyContainer()
        text_item = TextItem(
            pygame.Rect(0, 0, 120, 40),
            "abc",
            container,
            border_color=(10, 20, 30),
        )
        text_item.active = True
        text_item.cursor_pos = 2
        text_item.last_mouse_pos = (999, 999)

        surface = pygame.Surface((400, 300))

        with patch("pygame.draw.line") as mock_line:
            text_item.draw(surface)

        self.assertEqual(mock_line.call_args[0][1], text_item.text_color)
        expected_x = text_item.rect.x + text_item.padding + text_item.font.size("ab")[0]
        self.assertEqual(mock_line.call_args[0][2][0], expected_x)


if __name__ == "__main__":
    unittest.main()
