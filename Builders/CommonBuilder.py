

import pygame

from DataClasses.ButtonConfigData import ActionButtonPosition
from Model.Buttons.ButtonIcons.ActionButton import ActionButton


class CommonBuilder:

    def __init__(self, main_window):   
        self.main_window = main_window
        self.app_state = main_window.get_state()
        self.event_handler = self.main_window.get_event_handler()

    
    def build_action_buttons(self, target, action_buttons, config_pool):
        all_buttons = []
        
        if not action_buttons or len(action_buttons) == 0:
            return
        
        # Loop through actions
        for action_config in action_buttons:
            id_set = set(action_config.ConfigIds)
            button_config_list = [config for config in config_pool if config.Id in id_set]
           
            if action_config.Position == ActionButtonPosition.RIGHT:
                all_buttons += self.build_action_right(button_config_list, target)
            elif action_config.Position == ActionButtonPosition.TOP:
                all_buttons +=  self.build_action_top(button_config_list, target)           
       
        return all_buttons

    def build_action_top(self, buttons_config, target):
        buttons = []
        # Loop through the config array and build ActionButton
        button_offset_x = target.rect.x + 5
        button_offset_y = target.rect.y - 25

        for config in buttons_config:           
                            
            button_rect = pygame.Rect(button_offset_x, button_offset_y, config.size.width, config.size.height)
            action_button = ActionButton(button_rect, config, target,
                                         config.ignore_previous_offset_x, config.ignore_previous_offset_y)
            buttons.append(action_button)
            button_offset_x += config.size.width + 5 

             # register button for relevant events
            self.event_handler.subscribe(pygame.MOUSEMOTION, action_button)
            self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, action_button)
            
        return buttons

    def build_action_right(self, buttons_config, target):
        buttons = []
        # Loop through the config array and build ActionButton
        button_offset_x = target.rect.topright[0] + 10
        button_offset_y = target.rect.topright[1]
        previous_item_height = 0

        for config in buttons_config:
           
            # Check if config contains this attribute ignore_previous_offset_y and it has been set 
            if config.ignore_previous_offset_y is None or not config.ignore_previous_offset_y:
                button_offset_y += previous_item_height
                # update additoinal offset for next button
                previous_item_height =  config.size.height + 5               
           
            button_rect = pygame.Rect(button_offset_x,  button_offset_y, config.size.width, config.size.height)
            action_button = ActionButton(button_rect, config, target, config.ignore_previous_offset_x, config.ignore_previous_offset_y)
            buttons.append(action_button)
            
            # register button for relevant events
            self.event_handler.subscribe(pygame.MOUSEMOTION, action_button)
            self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, action_button)
            
        return buttons
