

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
    
    def build_basic_dialog(self):           
        title_font = pygame.font.SysFont(CommonDialogsConfig.DIALOG_TITLE_FONT[0], 
                                        CommonDialogsConfig.DIALOG_TITLE_FONT[1], bold=CommonDialogsConfig.DIALOG_TITLE_FONT[2])
        text_font = pygame.font.SysFont(CommonDialogsConfig.DIALOG_MESSAGE_FONT[0], 
                                        CommonDialogsConfig.DIALOG_MESSAGE_FONT[1])
        dialog_surface = pygame.Surface((400, 240), pygame.SRCALPHA)
        dialog_rect = dialog_surface.get_rect()
        dialog_rect.center = self.main_window.rect.center
        return BasicDialog(CommonDialogsConfig, dialog_surface,
                                    dialog_rect, self.main_window.get_canvass(), 
                                    title_font,text_font, self.main_window)
    

    
    def create_dialog_buttons(self, dialog_buttons_config, dialog_surface):
        width, height = dialog_surface.get_size()
        button_width = int(width * dialog_buttons_config[0].size_percent[0] // 100)      
        button_height = int(height * dialog_buttons_config[0].size_percent[1] // 100)

        gap = 10
        index = 0
        buttons = []
        for button_config in dialog_buttons_config: 
            x = index * (button_width + gap)
            y = height - 70  # Adjusted to position buttons at the bottom of the dialog
            button_font = pygame.font.SysFont(button_config.font[0], button_config.font[1])
            button = DialogButton(
                    pygame.Rect(x, y, button_width, button_height),
                    button_config.text,
                    button_font,
                    dialog_surface,
                    button_config.name,
                    button_config.bg_color
                )
            buttons.append(button)
            index += 1
        return buttons
    
