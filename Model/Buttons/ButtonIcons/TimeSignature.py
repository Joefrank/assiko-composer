
import pygame

from Model.Geometry.Line import Line
from Model.Geometry.Position import Position


class TimeSignature:

    def __init__(self, screen, parent, numerator_text, denominator_text, line_thickness, 
                 text_color, font):
        self.numerator_text = numerator_text
        self.denominator_text = denominator_text
        self.line_thickness = line_thickness
        self.text_color = text_color
        self.font = font
        self.numerator = None
        self.num_rect = None
        self.denominator = None
        self.denom_rect = None
        self.separator_line = None
        self.screen = screen
        self.parent = parent
        self.numerator_offset_y = 5
        self.denominator_offset_y = 20

    def build(self):
        self.build_fraction()
        self.separator_line = self.build_separator_line(self.parent.rect)
        self.set_position()
    
    def build_fraction(self):
        self.numerator = self.build_font(self.numerator_text)
        self.denominator = self.build_font(self.denominator_text)        
        # Calculate positions to stack them vertically
        self.num_rect = self.numerator.get_rect()
        self.denom_rect = self.denominator.get_rect()
     
    def build_separator_line(self, rect, y_offset = None):
        # Draw the line separator
        max_width = max(self.num_rect.width, self.denom_rect.width)
        half_parent_width = max_width // 2
        line_left = rect.centerx - half_parent_width - 2
        line_right = rect.centerx + half_parent_width + 2
        y = rect.centery if y_offset is None else y_offset
        start_position = Position(line_left, y)
        end_position = Position(line_right, y)
        return Line(start_position, end_position, self.line_thickness, self.text_color)

    def set_position(self):       
        # Center numerator horizontally at button center, positioned above line
        self.num_rect.centerx = self.parent.rect.centerx #- (max_width // 2)
        self.num_rect.y = self.parent.rect.y - (self.num_rect.height // 2) + self.numerator_offset_y        
        # Center denominator horizontally at button center, positioned below line
        self.denom_rect.centerx = self.parent.rect.centerx
        self.denom_rect.y = self.parent.rect.y - (self.denom_rect.height // 2) + self.denominator_offset_y

    """ Text is what is displayed on the button."""
    def build_font(self, text):
        return self.font.render(text, True, self.text_color)
    
    """ Builds a copy of the timesignature object. This is used when dragging symbol."""
    def build_dragged_copy(self, dragged_container_rect):
        # if self.parent.dragging:
        #     print(f"numerator:{self.num_rect.x, self.num_rect.y, self.num_rect.width, self.num_rect.height}")        
        numerator_rect_copy = self.build_fractional_part_copy(self.parent.text[0], self.num_rect, dragged_container_rect)
        line_copy = self.build_separator_line(dragged_container_rect, numerator_rect_copy.bottom + 2) 
        self.draw_line(line_copy)
        if  self.parent.dragging:
            print(f"deno:{self.denom_rect.x, self.denom_rect.y, self.denom_rect.width, self.denom_rect.height}")
        self.build_fractional_part_copy(self.parent.text[1], self.denom_rect, dragged_container_rect)
        
    def build_fractional_part_copy(self, symbol, part_rect, dragged_container_rect):
        part_rect_x_offset = part_rect.x - self.parent.rect.x
        part_rect_y_offset =  part_rect.y - self.parent.rect.y            
        part_rect_copy = self.font.render(symbol, True, self.text_color)            
        part_rect_copy_rect = part_rect_copy.get_rect()
        part_rect_copy_rect.center = (dragged_container_rect.x + part_rect_x_offset, 
                                      dragged_container_rect.y + part_rect_y_offset)
        self.screen.blit(part_rect_copy, part_rect_copy_rect)
        return part_rect_copy_rect
    
    def draw(self):
        self.screen.blit(self.numerator, self.num_rect)
        self.draw_line(self.separator_line)
        self.screen.blit(self.denominator, self.denom_rect)

    def resize(self, new_width_ratio, new_height_ratio):
        # change size of this font
        self.denominator_offset_y *= new_height_ratio
        self.numerator_offset_y *= new_height_ratio
        self.line_thickness = int(round(self.line_thickness * new_height_ratio))

    def update_font(self, font):
        self.font = font

    def draw_line(self, line:Line):
        pygame.draw.line(self.screen, line.color, line.start_position.get_tuple(), 
                         line.end_position.get_tuple(), line.thickness)
  
    