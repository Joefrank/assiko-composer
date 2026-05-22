

from dataclasses import dataclass


@dataclass
class TextInputBlinkTimer:
    NAME = "text_input_blink"
    INTERVAL = 500  # milliseconds
    ACTION = "toggle_cursor_visibility"