

import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Buttons.DialogButton import DialogButton
from Model.Control import Control

class BasicDialog(Control):

    def __init__(self, config, surface, rect, screen, title_font, content_font, parent):
        super().__init__(rect, ControlType.DIALOG, config.DIALOG_NAME, parent) 
        self.surface = surface
        self.screen = screen  
        self.title_font = title_font 
        self.text_font= content_font    
        self.title = None
        self.message = None
        self.config = config
        self.set_z_index(ControlZIndex.LEVEL4) 
        self.visible = False
        parent_size = self.parent.get_size()

        # Dark transparent background
        self.overlay = pygame.Surface(
            (parent_size.width, parent_size.height),
            pygame.SRCALPHA
        )

        self.overlay.fill((0, 0, 0, 160))

        button_y = self.rect.bottom - 70
        
        self.yes_button = DialogButton(
            pygame.Rect(
                self.rect.width // 2 - 140,
                button_y,
                110,
                45
            ),
            "Yes",
            self.text_font,
            self.surface,
            "Yes button",
            (50, 170, 80)
        )

        self.no_button = DialogButton(
             pygame.Rect(
                self.rect.width // 2 + 30,
                button_y,
                110,
                45
            ),
            "No",
            self.text_font,
            self.surface,
            "No button",
            (190, 70, 70)
        )

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width, height):
        self.rect.width = width
        self.rect.height = height
        self.size = (width, height)

    def set_content(self, title, main_content):
        self.title = title
        self.message = main_content

    def draw(self):
        # fill dialog background
        self.surface.fill(self.config.BACKGROUND_COLOR)

        # draw border
        #pygame.draw.rect(self.surface, self.config.BORDER_COLOR, self.rect, 10, 10)     
        

        # draw title text
        title_font = self.title_font.render(self.title, True, self.config.TEXT_COLOR)
        self.surface.blit(title_font, (20, 10))

        self.yes_button.draw()
        self.no_button.draw()

        # draw message text
        message_font = self.text_font.render(self.message, True, self.config.TEXT_COLOR)
        self.surface.blit(message_font, (20, (self.rect.height // 3) - 10))

        # draw dialog onto main screen
        self.screen.blit(self.surface, self.rect)
       
