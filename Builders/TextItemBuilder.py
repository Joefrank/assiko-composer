
import pygame

from DataClasses.Config.EventsConfig import TextInputBlinkTimer
from Model.Inputs.TextInput import TextInput
from Model.Inputs.TextItem import TextItem


class TextItemBuilder:

    def __init__(self, main_window): 
        self.main_window = main_window
        self.event_handler = self.main_window.get_event_handler()

    def build_text_item(self, rect, parent_page):
        text_item= TextItem(rect, "Click and type", parent_page, bg_color=(250,250,250), text_color=(100,100,100))
        #self.event_handler.subscribe(pygame.MOUSEMOTION, text_item)
        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, text_item)
        self.event_handler.subscribe(pygame.KEYDOWN, text_item)
        self.event_handler.subscribe_timer(TextInputBlinkTimer.NAME, text_item)
        return text_item
    
    def build_text_input(self, rect, parent_page):
        name = f"TextInput_{len(parent_page.children)}"
        text_input = TextInput(parent_page, rect, name)
        self.event_handler.subscribe(pygame.MOUSEMOTION, text_input)
        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, text_input)
        self.event_handler.subscribe(pygame.KEYDOWN, text_input)
        self.event_handler.subscribe_timer(TextInputBlinkTimer.NAME, text_input)
        return text_input
    