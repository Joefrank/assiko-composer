
from abc import abstractmethod

import pygame

from Model.Buttons.Button import Button
from Model.Buttons.ImageButton import ImageButton
from Model.Buttons.StaggeredLabelButton import StaggeredLabelButton
from Model.Buttons.TimeSignatureButton import TimeSignatureButton


class ButtonBuilder: 
 
    @abstractmethod 
    def build_button(self, screen, toolbar, action, icon, font, font_details, border_radius, text_color,
                             bg_color, hover_text_color, hover_bg_color, draggable_icons, position) -> Button:
        pass

class SimpleButtonBuilder(ButtonBuilder):

    def build_button(self, screen, toolbar, action, icon, font, font_details, border_radius, text_color,
                             bg_color, hover_text_color, hover_bg_color, draggable_icons, position):
        
        rect = pygame.Rect(position[0], position[1], toolbar.button_width, toolbar.button_height)
           
        button = Button(screen, action, rect, icon, action, font, font_details, border_radius, toolbar.button_text_center,
                        text_color, bg_color, hover_text_color, hover_bg_color, draggable_icons)
        
        button.set_parent(toolbar, offset_x=position[0], offset_y=position[1])

        return button
    
class ImageButtonBuilder(SimpleButtonBuilder):
     
     def build_button(self, screen, toolbar, action, icon, font, font_details, border_radius, text_color,
                             bg_color, hover_text_color, hover_bg_color, draggable_icons, position):
        
        rect = pygame.Rect(position[0], position[1], toolbar.button_width, toolbar.button_height)
           
        button = ImageButton(screen, action, rect, icon, action, font, font_details, border_radius, toolbar.button_text_center,
                        text_color, bg_color, hover_text_color, hover_bg_color, draggable_icons)
        
        button.set_parent(toolbar, offset_x=position[0], offset_y=position[1])

        return button

class TimeSignatureButtonBuilder(SimpleButtonBuilder):
   
   def build_button(self, screen, toolbar, action, icon, font, font_details, border_radius, text_color,
                             bg_color, hover_text_color, hover_bg_color, draggable_icons, position):
      
       rect = pygame.Rect(position[0], position[1], toolbar.button_width, toolbar.button_height)

       button = TimeSignatureButton(screen, action, rect, icon, action, font, font_details, border_radius, 
                                    toolbar.button_text_center, text_color, bg_color, hover_text_color, 
                                    hover_bg_color, draggable_icons)
       
       button.set_parent(toolbar, offset_x=position[0], offset_y=position[1])
       button.build_signature_symbols()
       
       return button
        
class StaggeredSymbolButtonBuilder(SimpleButtonBuilder):

    def build_button(self, screen, toolbar, action, icon, font, font_details, border_radius, text_color,
                             bg_color, hover_text_color, hover_bg_color, draggable_icons, position):
       symbols = []
       for i in range(icon[1]):
            symbols.append(icon[0])

       rect = pygame.Rect(position[0], position[1], toolbar.button_width, toolbar.button_height)

       button = StaggeredLabelButton(screen, action, rect, icon, action, font, font_details, border_radius, toolbar.button_text_center,
                        text_color, bg_color, hover_text_color, hover_bg_color, draggable_icons, symbols)
       button.set_parent(toolbar, offset_x=position[0], offset_y=position[1])
       
       button.rect.width = button.build_staggered_symbols()

       return button