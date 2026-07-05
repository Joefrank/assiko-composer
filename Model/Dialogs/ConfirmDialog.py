
import pygame

from Model.Dialogs.BasicDialog import BasicDialog


class ConfirmDialog(BasicDialog):

    def __init__(self, config, surface, rect, screen, title_font, text_font, parent, action_buttons): # pass button config here , yes_text="Yes", no_text="Cancel"
        super().__init__(config, surface, rect, screen, title_font, text_font, parent) 
        self.action_buttons = action_buttons
        


        