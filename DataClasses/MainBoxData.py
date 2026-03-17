from dataclasses import dataclass

@dataclass
class MainBoxConfig:
    TOP_OFFSET_RATIO = 0.26  # based on MENU_BAR_HEIGHT_RATIO + TOOLBAR_HEIGHT_RATIO * 2
    HEIGHT_RATIO = 0.7
    WIDTH_RATIO = 0.8
    NAME = "MainScoreBox"
    BAR_SIZE = 8
    SCROLL_SPEED = 40
    BG_COLOR = (245, 245, 245)
    BAR_BG = (0, 0, 0, 0)  # invisible track
    TEXT_COLOR = (10,10, 10)
    HIGHLIGHT_COLOR = (200, 200, 255)
    HIGHLIGHT_COLOR=(200, 200, 255),
    CONTAINER_COLOR=(220, 220, 220)
    BAR_THUMB = (60, 60, 60, 160)
    BAR_THUMB_HOVER = (60, 60, 60, 220)