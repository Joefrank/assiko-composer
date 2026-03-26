

import pygame

from DataClasses.ButtonConfigData import ButtonConfig
from Model.Buttons.Button import Button


class ButtonConfigMapper:

    @staticmethod
    def map_config_to_simplebutton_params(config: ButtonConfig):
        rect = ButtonConfigMapper.get_rect(config)
       
        return Button(config.screen, config.action, rect, config.icon, config.action, config.font, config.font_details,
                       config.border_radius, None, config.text_color, config.hover_text_color, 
                       config.hover_bg_color, config.draggable_icons, config.action_value)
    @staticmethod
    def get_rect(config: ButtonConfig):
        return pygame.Rect(config.position[0], config.position[1], config.toolbar.button_width,
                            config.toolbar.button_height)