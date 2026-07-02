

import pygame

from DataClasses.DialogConfigData import CommonDialogsConfig
from Model.Buttons.DialogButton import DialogButton
from Model.Containers.Window import Window
from Model.Dialogs.BasicDialog import BasicDialog

class DialogBuilder:
    
    def __init__(self, main_window:Window):  
        self.main_window = main_window  

    def build(self):
        return self.build_basic_dialog()
    
    def calculate_dialog_dimensions(self, width_ratio, height_ratio):
        main_window_width, main_window_height = self.main_window.rect.size
        dialog_width = int(main_window_width * width_ratio // 100)
        dialog_height = int(main_window_height * height_ratio // 100)
        return dialog_width, dialog_height
    
    def build_basic_dialog(self):           
        title_font = pygame.font.SysFont(CommonDialogsConfig.DIALOG_TITLE_FONT[0], 
                                        CommonDialogsConfig.DIALOG_TITLE_FONT[1], bold=CommonDialogsConfig.DIALOG_TITLE_FONT[2])
        text_font = pygame.font.SysFont(CommonDialogsConfig.DIALOG_MESSAGE_FONT[0], 
                                        CommonDialogsConfig.DIALOG_MESSAGE_FONT[1])
        
        dialog_width, dialog_height = self.calculate_dialog_dimensions(CommonDialogsConfig.DIALOG_SIZE_PERCENT[0], 
                                                                       CommonDialogsConfig.DIALOG_SIZE_PERCENT[1])
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        dialog_rect = dialog_surface.get_rect()
        dialog_rect.center = self.main_window.rect.center
        return BasicDialog(CommonDialogsConfig, dialog_surface,
                                    dialog_rect, self.main_window.get_canvass(), 
                                    title_font,text_font, self.main_window)
    

    def calculate_first_button_position(self, dialog_width, dialog_height, button_width, button_height, num_buttons):
        total_button_width = num_buttons * button_width
        gap = 10  # Gap between buttons
        total_gap_width = (num_buttons - 1) * gap
        total_width = total_button_width + total_gap_width

        x_start = (dialog_width - total_width) // 2
        y_position = dialog_height - 70  # 20 pixels from the bottom of the dialog

        return x_start, y_position
    
    def create_dialog_buttons(self, dialog_buttons_config, dialog, callbacks=None):
        width, height = dialog.surface.get_size()
        if not dialog_buttons_config:
            return []

        sample_button_config = dialog_buttons_config[0]
        button_width = int(width * sample_button_config.size_percent[0] // 100)
        button_height = int(height * sample_button_config.size_percent[1] // 100)
        x_start, y_position = self.calculate_first_button_position(width, height, button_width, button_height,
                                                                   len(dialog_buttons_config))
        gap = 10
        index = 0
        buttons = []

        if callbacks is None:
            callbacks = []

        for button_config in dialog_buttons_config:
            x = x_start + (index * (button_width + gap))

            button_font = pygame.font.SysFont(button_config.font[0], button_config.font[1], bold=button_config.font[2] if len(button_config.font) > 2 else False)
            button = DialogButton(
                    pygame.Rect(x, y_position, button_width, button_height),
                    button_config.text,
                    button_font,
                    button_config.name,
                    dialog,
                    background_color=button_config.bg_color,
                    text_color=button_config.text_color
                )
            if callbacks:
                callback = callbacks[index] if index < len(callbacks) else None
                button.set_action(callback)
            buttons.append(button)
            index += 1
        return buttons
    
