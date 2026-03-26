
from abc import abstractmethod

import pygame

from DataClasses.ButtonConfigData import ButtonConfig
from Helpers.ButtonMapper import ButtonConfigMapper
from Model.Buttons.Button import Button
from Model.Buttons.ImageButton import ImageButton
from Model.Buttons.StaggeredLabelButton import StaggeredLabelButton
from Model.Buttons.TimeSignatureButton import TimeSignatureButton


class ButtonBuilder: 
    
    def __init__(self):
        self.button_rect = None

    @abstractmethod 
    def build_button2(self, config: ButtonConfig) -> Button:
        self.get_rect(config)
    
    @abstractmethod
    def create_button(self, config: ButtonConfig) -> Button:
        pass

    def build_rect(self, position:tuple, toolbar):
        return pygame.Rect(position[0], position[1], toolbar.button_width, toolbar.button_height)
            


class SimpleButtonBuilder(ButtonBuilder):
        
    def create_button(self, config: ButtonConfig) -> Button:
        return Button(config)        
    
class ImageButtonBuilder(SimpleButtonBuilder):

    def create_button(self, config: ButtonConfig) -> ImageButton:
        return ImageButton(config)
    

class TimeSignatureButtonBuilder(SimpleButtonBuilder):

    def create_button(self, config: ButtonConfig) -> TimeSignatureButton:
        button = TimeSignatureButton(config)
        button.set_parent(config.toolbar, offset_x=config.position[0], offset_y=config.position[1])
        button.build_signature_symbols()
       
        return button

class StaggeredSymbolButtonBuilder(SimpleButtonBuilder):
    
    def create_button(self, config: ButtonConfig) -> StaggeredLabelButton:
        symbols = []
        for i in range(config.icon[1]):
            symbols.append(config.icon[0])

        button = StaggeredLabelButton(config, symbols)
        button.set_parent(config.toolbar, offset_x=config.position[0], offset_y=config.position[1])
        button.rect.width = button.build_staggered_symbols()
       
        return button