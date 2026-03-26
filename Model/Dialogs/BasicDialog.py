

import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Control import Control


class BasicDialog(Control):

    def __init__(self, name, surface, rect, screen, font):
        super().__init__(rect, ControlType.DIALOG, name) 
        self.surface = surface
        self.screen = screen  
        self.font = font     
        self.title = None
        self.content = None
        self.set_z_index(ControlZIndex.LEVEL4) 
        self.visible = False

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width, height):
        self.rect.width = width
        self.rect.height = height
        self.size = (width, height)

    def set_content(self, title, main_content):
        self.title = title
        self.content = main_content

    def draw(self):
        # fill dialog background
        self.surface.fill((50, 50, 50))

        # draw border
        pygame.draw.rect(self.surface, (200, 200, 200), self.rect, 2)

        # draw text
        text = self.font.render(self.content, True, (255, 255, 255))
        self.surface.blit(text, (20, 60))

        # draw dialog onto main screen
        self.screen.blit(self.surface, self.rect)




