

from DataClasses.ButtonData import ButtonConfig
from Helpers.ScreeHelper import ScreenHelper
from Model.Buttons.Button import Button
from Model.Geometry.Line import Line
from Model.Geometry.Position import TextPosition
import pygame

from Model.Buttons.ButtonIcons.TimeSignature import TimeSignature


class TimeSignatureButton(Button):
   
    def __init__(self, screen, name, rect, text, action, font, font_details, border_radius=0, text_position=TextPosition.CENTER,
                 text_color=ButtonConfig.TEXT_DEFAULT_COLOR, bg_color=ButtonConfig.BTN_DEFAULT_COLOR, hover_text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
                 hover_bg_color=ButtonConfig.BTN_DEFAULT_HOVER, is_draggable=False):
           super().__init__(screen, name, rect, text, action, font, font_details, border_radius, text_position,
                 text_color, bg_color, hover_text_color, hover_bg_color, is_draggable)           
           self.line_thickness = 1
           self.line_spacing = 2      
           self.signature = TimeSignature(screen, self, self.text[0], self.text[1], 
                                          self.line_thickness, self.text_color, font)
          

    """For time signature, the label is a tuple with 2 elements top and bottom"""  
    def build_signature_symbols(self):
        self.signature.build()        

    def draw_label(self, text_color):
        self.signature.draw()
       
    def resize(self, new_width_ratio, new_height_ratio):
        # change size of this font        
        self.font_details = (self.font_details[0], int(self.font_details[1] * new_height_ratio))
        self.font = ScreenHelper.create_font(self.font_details) 
        self.signature.resize(new_width_ratio, new_height_ratio)
        self.signature.update_font(self.font)               
        return super().resize_only(new_width_ratio, new_height_ratio)
    
    def reposition_children(self, new_width_ratio, new_height_ratio):
        self.signature.build()  
    
    def draw_dragged_icons(self):       
        for dragged_note in self.dragged_symbols: 
            self.signature.build_dragged_copy(dragged_note)  

    def draw_line(self, line:Line):
        pygame.draw.line(self.screen, line.color, line.start_position.get_tuple(), 
                         line.end_position.get_tuple(), line.thickness)
            
             
              
