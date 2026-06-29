

import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
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

        

        # Shadow
        # shadow = self.rect.move(5, 5)
        # pygame.draw.rect(
        #     self.surface,
        #     (0, 0, 0),
        #     shadow,
        #     border_radius=18
        # )
        # print(self.rect)

        # # Main dialog
        # pygame.draw.rect(
        #     self.screen,
        #     (35, 38, 45),
        #     self.rect,
        #     border_radius=18
        # )

        # draw title text
        title_font = self.title_font.render(self.title, True, self.config.TEXT_COLOR)
        self.surface.blit(title_font, (20, 10))

        # draw message text
        message_font = self.text_font.render(self.message, True, self.config.TEXT_COLOR)
        self.surface.blit(message_font, (20, (self.rect.height // 3) - 10))

        # draw dialog onto main screen
        self.screen.blit(self.surface, self.rect)

    # def draw(self):
        # self.surface.blit(self.overlay, (0, 0))

        # # Shadow
        # shadow = self.rect.move(5, 5)
        # pygame.draw.rect(
        #     self.surface,
        #     (0, 0, 0),
        #     shadow,
        #     border_radius=18
        # )

        # # Main dialog
        # pygame.draw.rect(
        #     self.surface,
        #     (35, 38, 45),
        #     self.rect,
        #     border_radius=18
        # )

        # pygame.draw.rect(
        #     self.surface,
        #     (80, 140, 255),
        #     self.rect,
        #     2,
        #     border_radius=18
        # )

        # title_content = self.title_font.render(
        #     self.title,
        #     True,
        #     (255, 255, 255)
        # )

        # message_content = self.text_font.render(
        #     self.message,
        #     True,
        #     (220, 220, 220)
        # )

        # self.surface.blit(
        #     title_content,
        #     (self.rect.x + 25, self.rect.y + 20)
        # )

        # self.surface.blit(
        #     message_content,
        #     (self.rect.x + 25, self.rect.y + 90)
        # )




