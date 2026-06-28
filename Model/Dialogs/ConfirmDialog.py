
import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Buttons.DialogButton import DialogButton
from Model.Control import Control


class ConfirmDialog(Control):

    def __init__(self, config, surface, rect, screen, title_font, text_font, parent): # pass button config here , yes_text="Yes", no_text="Cancel"
        super().__init__(rect, ControlType.DIALOG, config.DIALOG_NAME, parent) 
        self.surface = surface
        self.main_screen = screen
        self.title = None
        self.message = None
        self.title_font = title_font
        self.text_font = text_font
        self.result = None
        self.config = config
        self.set_z_index(ControlZIndex.LEVEL4) 
        self.visible = False
        button_y = self.rect.bottom - 70


        self.yes_button = DialogButton(
            pygame.Rect(self.rect.centerx - 140, button_y, 110, 45),
            "Yes",
            self.text_font,
            self.surface,
            "Yes button",
            (50, 170, 80)
        )

        self.no_button = DialogButton(
            pygame.Rect(self.rect.centerx + 30, button_y, 110, 45),
            "No",
            self.text_font,
            self.surface,
            "No button",
            (190, 70, 70)
        )

        parent_size = self.parent.get_size()

        # Dark transparent background
        self.overlay = pygame.Surface(
            (parent_size.width, parent_size.height),
            pygame.SRCALPHA
        )

        self.overlay.fill((0, 0, 0, 160))

    def handle_event(self, event):
        # ESC acts as No
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.result = False
                self.visible = False

        if self.yes_button.handle_event(event):
            self.result = True
            self.visible = False

        if self.no_button.handle_event(event):
            self.result = False
            self.visible = False

        # Consume all events
        return True

    def set_size(self, width, height):
        self.rect.width = width
        self.rect.height = height
        self.size = (width, height)

    def set_content(self, title, main_content):
        self.title = title
        self.message = main_content

    def draw(self):
        self.surface.blit(self.overlay, (0, 0))

        # Shadow
        shadow = self.rect.move(5, 5)
        pygame.draw.rect(
            self.surface,
            (0, 0, 0),
            shadow,
            border_radius=18
        )

        # Main dialog
        pygame.draw.rect(
            self.surface,
            (35, 38, 45),
            self.rect,
            border_radius=18
        )

        pygame.draw.rect(
            self.surface,
            (80, 140, 255),
            self.rect,
            2,
            border_radius=18
        )

        title_content = self.title_font.render(
            self.title,
            True,
            (255, 255, 255)
        )

        message_content = self.text_font.render(
            self.message,
            True,
            (220, 220, 220)
        )

        self.surface.blit(
            title_content,
            (self.rect.x + 25, self.rect.y + 20)
        )

        self.surface.blit(
            message_content,
            (self.rect.x + 25, self.rect.y + 90)
        )

        self.yes_button.draw()
        self.no_button.draw()

