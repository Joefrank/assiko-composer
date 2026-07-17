
import pygame

from Model.DragAndDrop.TextItem import TextItem


class TextItemBuilder:

    def __init__(self, main_window): 
        self.main_window = main_window

    def build_text_item(self, rect, parent_page):
        item_rect = pygame.Rect(rect.x, rect.y, 200, 50)
        return TextItem(item_rect, "...", parent_page, bg_color=(250,250,250), text_color=(100,100,100))