
from Model.Geometry.Line import Line
from Model.Geometry.Position import Position


class TimeSignature:

    def __init__(self, parent, numerator_text, denominator_text, line_thickness, 
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
        self.parent = parent

    def build(self):
        self.build_fraction()
        self.build_separator_line()

    def build_fraction(self):
        self.numerator = self.build_font(self.numerator_text)
        self.denominator = self.build_font(self.denominator_text)        
        # Calculate positions to stack them vertically
        self.num_rect = self.numerator.get_rect()
        self.denom_rect = self.denominator.get_rect()
     
    def build_separator_line(self):
        # Draw the line separator
        half_parent_width = self.parent.rect.width // 2
        line_left = self.parent.centerx - half_parent_width - 2
        line_right = self.parent.centerx + half_parent_width + 2
        start_position = Position(line_left, self.parent.centery)
        end_position = Position(line_right, self.parent.centery)
        self.separator_line = Line(start_position, end_position, self.line_thickness, self.text_color)

    def set_position(self):
        # Get the max width to center both numerator and denominator
        max_width = max(self.num_rect.width, self.denom_rect.width)
       
        # Center numerator horizontally at button center, positioned above line
        self.num_rect.centerx = self.rect.centerx #- (max_width // 2)
        self.num_rect.y = self.rect.y - (self.num_rect.height // 2) + self.numerator_offset_y
        
        # Center denominator horizontally at button center, positioned below line
        self.denom_rect.centerx = self.rect.centerx
        self.denom_rect.y = self.rect.y - (self.denom_rect.height // 2) + self.denominator_offset_y

    def resize(self, new_width_ratio, new_height_ratio):
        pass
        # change size of this font
        # self.denominator_offset_y *= new_height_ratio
        # self.numerator_offset_y *= new_height_ratio
        # self.font_details = (self.font_details[0], int(self.font_details[1] * new_height_ratio))
        # self.font = ScreenHelper.create_font(self.font_details) 
        # self.build_signature_symbols() # This is necessary because of fonts    
        # return super().resize_only(new_width_ratio, new_height_ratio)

    def build_font(self, text):
        return self.font.render(text, True, self.text_color)
  
    