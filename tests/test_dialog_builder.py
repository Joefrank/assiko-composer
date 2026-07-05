import os
import sys
import pygame
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Builders.DialogBuilder import DialogBuilder


class DummyMainWindow:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 400, 300)

    def get_canvass(self):
        return pygame.Surface((400, 300))


class DummyDialog:
    def __init__(self):
        self.surface = pygame.Surface((200, 200), pygame.SRCALPHA)


class DummyButtonConfig:
    def __init__(self, text="OK"):
        self.size_percent = (50, 30)
        self.font = ("arial", 16, True)
        self.text = text
        self.name = text.lower()
        self.bg_color = (100, 100, 100)
        self.text_color = (255, 255, 255)


class DialogBuilderCallbackTests(unittest.TestCase):
    def test_create_dialog_buttons_assigns_callbacks(self):
        builder = DialogBuilder(DummyMainWindow())
        dialog = DummyDialog()
        calls = []

        buttons = builder.create_dialog_buttons(
            [DummyButtonConfig("OK")],
            dialog,
            callbacks=[lambda: calls.append("clicked")],
        )

        self.assertEqual(len(buttons), 1)
        self.assertIsNotNone(buttons[0].action)
        buttons[0].on_left_mouse_down(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=buttons[0].rect.topleft))
        self.assertEqual(calls, ["clicked"])


if __name__ == "__main__":
    unittest.main()
