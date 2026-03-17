

from DataClasses.ButtonData import ButtonConfig
from Model.Button import Button
from Model.Position import TextPosition
import pygame


class TimeSignatureButton(Button):
    
    def __init__(self, screen, name, rect, text, action, font, font_details, border_radius=0, text_position=TextPosition.CENTER,
                 text_color=ButtonConfig.TEXT_DEFAULT_COLOR, bg_color=ButtonConfig.BTN_DEFAULT_COLOR, hover_text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
                 hover_bg_color=ButtonConfig.BTN_DEFAULT_HOVER, is_draggable=False):
           super().__init__(screen, name, rect, text, action, font, font_details, border_radius, text_position,
                 text_color, bg_color, hover_text_color, hover_bg_color, is_draggable)

    """For time signature, the label is a tuple with 2 elements top and bottom"""  
    def draw_label(self, text_color):
        # Render numerator (top) and denominator (bottom)
        numerator = self.font.render(self.text[0], True, text_color)
        denominator = self.font.render(self.text[1], True, text_color)
        
        # Calculate positions to stack them vertically
        num_rect = numerator.get_rect()
        denom_rect = denominator.get_rect()
        
        # Get the max width to center both
        max_width = max(num_rect.width, denom_rect.width)
        line_thickness = 1
        line_spacing = 2  # gap between line and numbers
        
        # Center numerator horizontally at button center, positioned above line
        num_rect.centerx = self.rect.centerx
        num_rect.y = self.rect.y - (num_rect.height // 2) + 20
        
        # Center denominator horizontally at button center, positioned below line
        denom_rect.centerx = self.rect.centerx
        denom_rect.y = self.rect.y - (denom_rect.height // 2) + 5 #(self.rect.height // 2)
        
        # Draw the line separator
        line_y = self.rect.centery
        line_left = self.rect.centerx - max_width // 2 - 2
        line_right = self.rect.centerx + max_width // 2 + 2
        pygame.draw.line(self.screen, text_color, (line_left, line_y), (line_right, line_y), line_thickness)
        
        # Blit numerator and denominator
        self.screen.blit(numerator, num_rect)
        self.screen.blit(denominator, denom_rect)