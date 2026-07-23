
import pygame

from Builders.CommonBuilder import CommonBuilder
from DataClasses.ButtonConfigData import STAFF_ACTION_BUTTON_CONFIG, TEXT_ITEM_ACTION_BUTTON_CONFIG
from DataClasses.Config.EventsConfig import TextInputBlinkTimer
from Model.Buttons.ButtonIcons.ActionButton import ActionButton
from Model.Inputs.TextInput import TextInput
from Model.Inputs.TextItem import TextItem


class TextItemBuilder(CommonBuilder):

    def __init__(self, main_window): 
        super().__init__(main_window)   
       

    def build_text_item(self, rect, parent_page, action_buttons_conf=[]):
        text_item= TextItem(rect, "Click and type", parent_page, bg_color=(255,250,252), text_color=(100,100,100),
                            inactive_border_thickness=1)

        if action_buttons_conf and len(action_buttons_conf) > 0:
            action_buttons = self.build_action_buttons(text_item, action_buttons_conf, TEXT_ITEM_ACTION_BUTTON_CONFIG)
            text_item.children += action_buttons
            text_item.action_buttons = action_buttons            

        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, text_item)
        self.event_handler.subscribe(pygame.KEYDOWN, text_item)
        self.event_handler.subscribe_timer(TextInputBlinkTimer.NAME, text_item)
        return text_item

    # def _attach_text_item_action_buttons(self, text_item, action_buttons=[]):
    #     buttons = []
    #     button_offset_x = text_item.rect.right + 10
    #     button_offset_y = text_item.rect.y + 2

    #     for config in TEXT_ITEM_ACTION_BUTTON_CONFIG:
    #         button_rect = pygame.Rect(button_offset_x, button_offset_y, config.size.width, config.size.height)
    #         action_button = ActionButton(button_rect, config, text_item)
    #         buttons.append(action_button)
    #         self.event_handler.subscribe(pygame.MOUSEMOTION, action_button)
    #         self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, action_button)
    #         button_offset_y += config.size.height + 2

    #     text_item.action_buttons = buttons
    #     text_item.add_children(buttons)
    
    # def build_text_input(self, rect, parent_page):
    #     name = f"TextInput_{len(parent_page.children)}"
    #     text_input = TextInput(parent_page, rect, name)
    #     self.event_handler.subscribe(pygame.MOUSEMOTION, text_input)
    #     self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, text_input)
    #     self.event_handler.subscribe(pygame.KEYDOWN, text_input)
    #     self.event_handler.subscribe_timer(TextInputBlinkTimer.NAME, text_input)
    #     return text_input
    