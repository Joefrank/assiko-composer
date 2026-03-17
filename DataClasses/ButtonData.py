

from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class ButtonConfig:
    BTN_DEFAULT_COLOR = (70, 70, 70)
    BTN_DEFAULT_HOVER = (100, 100, 100)
    TEXT_DEFAULT_COLOR = (255, 255, 255)    


class ButtonType(Enum):
    BUTTON = auto()
    TIME_SIGNATURE_BUTTON = auto()
    STAGGERED_SYMBOL_BUTTON = auto()
    