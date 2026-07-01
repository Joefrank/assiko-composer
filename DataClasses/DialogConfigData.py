
  
from dataclasses import dataclass
from Assets.Languages.enGB.DialogButtonText import DialogButtonText


@dataclass(frozen=True)
class DialogButtonConfig:
    text: str
    name: str
    size_percent: tuple[int, int] # percentage width, height
    font: tuple[str, int] # font-name and size
    text_color: tuple[int, int, int]
    bg_color: tuple[int, int, int]
    border_radius: int

@dataclass
class DialogButtonsConfigs:
    OK_BUTTON = DialogButtonConfig(
        text=DialogButtonText.OK_Button_Label,
        name="OK Button",
        size_percent=(20, 22),
        font=("Segoe UI", 24),
        text_color=(255, 255, 255),
        bg_color=(125, 25, 25),
        border_radius=10,
    )
    CANCEL_BUTTON = DialogButtonConfig(
        text=DialogButtonText.Cancel_Button_Label,
        name="Cancel Button",
        size_percent=(20, 22),
        font=("Segoe UI", 24),
        text_color=(255, 255, 255),
        bg_color=(25, 25, 25),
        border_radius=10,
    )
    CONFIRM_BUTTON = DialogButtonConfig(
        text=DialogButtonText.Confirm_Button_Label,
        name="Confirm Button",
        size_percent=(20, 22),
        font=("Segoe UI", 24),
        text_color=(255, 255, 255),
        bg_color=(125, 80, 80),
        border_radius=10,
    )

@dataclass
class CommonDialogsConfig:
    DIALOG_SIZE_PERCENT = (40, 20) # these are percentages
    DIALOG_NAME = "Common Dialog"
    DIALOG_TITLE_FONT = ("Segoe UI", 34, True) # (font-name, size, bold)
    DIALOG_MESSAGE_FONT = ("Segoe UI", 24)
    DIALOG_BUTTONS_CONFIG = [DialogButtonsConfigs.OK_BUTTON]
    BACKGROUND_COLOR = (135, 138, 45)
    BORDER_COLOR = (100, 100, 100)
    TEXT_COLOR = (255, 255, 255)

@dataclass
class ConfirmDialogsConfig:
    DIALOG_SIZE_PERCENT = (40, 20) # these are percentages
    DIALOG_NAME = "Confirm Dialog"
    DIALOG_TITLE_FONT = ("Segoe UI", 34, True)
    DIALOG_MESSAGE_FONT = ("Segoe UI", 24)
    DIALOG_BUTTONS_CONFIG = [DialogButtonsConfigs.CONFIRM_BUTTON, DialogButtonsConfigs.CANCEL_BUTTON]
