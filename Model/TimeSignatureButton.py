

from DataClasses.ButtonData import ButtonConfig
from Helpers.ScreeHelper import ScreenHelper
from Model.Button import Button
from Model.Geometry.Line import Line
from Model.Geometry.Position import Position, TextPosition
import pygame


class TimeSignatureButton(Button):
   
    def __init__(self, screen, name, rect, text, action, font, font_details, border_radius=0, text_position=TextPosition.CENTER,
                 text_color=ButtonConfig.TEXT_DEFAULT_COLOR, bg_color=ButtonConfig.BTN_DEFAULT_COLOR, hover_text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
                 hover_bg_color=ButtonConfig.BTN_DEFAULT_HOVER, is_draggable=False):
           super().__init__(screen, name, rect, text, action, font, font_details, border_radius, text_position,
                 text_color, bg_color, hover_text_color, hover_bg_color, is_draggable)
           self.num_rect = None
           self.denom_rect = None
           self.line_thickness = 1
           self.line_spacing = 2
           self.numerator_offset_y = 5
           self.denominator_offset_y = 20
           self.separation_line = None
    
    ### TODO: use TimeSignature object for this

    """For time signature, the label is a tuple with 2 elements top and bottom"""  
    def build_signature_symbols(self):
        # Render numerator (top) and denominator (bottom)
        numerator = self.font.render(self.text[0], True, self.text_color)
        denominator = self.font.render(self.text[1], True, self.text_color)
        
        # Calculate positions to stack them vertically
        self.num_rect = numerator.get_rect()
        self.denom_rect = denominator.get_rect()
        self.children.clear()
        self.children.append((numerator, self.num_rect, self.text[0]))
        self.children.append((denominator, self.denom_rect, self.text[1]))
        

    def draw_label(self, text_color):
       
        # Center numerator horizontally at button center, positioned above line
        self.num_rect.centerx = self.rect.centerx
        self.num_rect.y = self.rect.y - (self.num_rect.height // 2) + self.numerator_offset_y
        
        # Center denominator horizontally at button center, positioned below line
        self.denom_rect.centerx = self.rect.centerx
        self.denom_rect.y = self.rect.y - (self.denom_rect.height // 2) + self.denominator_offset_y

        self.separation_line = self.build_separator_line(self.rect)       
        self.draw_line(self.separation_line)
        
        for child in self.children:       
            self.screen.blit(child[0], child[1])
         
    def build_separator_line(self, container_rect):
        # Get the max width to center both
        max_width = max(self.num_rect.width, self.denom_rect.width)
       
        # Build and return the line separator
        line_y = container_rect.centery
        half_width = max_width // 2
        line_left = container_rect.centerx - half_width - 2
        line_right = container_rect.centerx + half_width + 2
        start_position = Position(line_left, line_y)
        end_position = Position(line_right, line_y)

        return Line(start_position, end_position, self.line_thickness, self.text_color)
        
    def resize(self, new_width_ratio, new_height_ratio):
        # change size of this font
        self.denominator_offset_y *= new_height_ratio
        self.numerator_offset_y *= new_height_ratio
        self.font_details = (self.font_details[0], int(self.font_details[1] * new_height_ratio))
        self.font = ScreenHelper.create_font(self.font_details) 
        self.build_signature_symbols() # This is necessary because of fonts    
        return super().resize_only(new_width_ratio, new_height_ratio)
    
    def draw_dragged_icons(self):       
        for dragged_note in self.dragged_symbols: 
            # move children copies 
            child_count = 0         
            for child in self.children:
                x_offset = child[1].x - self.rect.x
                y_offset = child[1].y - self.rect.y
                child_copy = self.font.render(child[2], True, self.text_color)
                child_copy_rect = child_copy.get_rect()
                child_copy_rect.center = (dragged_note.x + x_offset +5, dragged_note.y + (child_count * self.denominator_offset_y))
                self.screen.blit(child_copy, child_copy_rect) 

                # create a line copy as well after first child
                if child_count == 0:
                    line = self.build_separator_line(dragged_note) 
                    self.draw_line(line)
                    print(f"dragged:{dragged_note} - child_copy:{child_copy_rect}")
                child_count += 1

    def draw_line(self, line:Line):
        pygame.draw.line(self.screen, line.color, line.start_position.get_tuple(), 
                         line.end_position.get_tuple(), line.thickness)
            
             
              
