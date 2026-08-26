
import pygame

from DataClasses.Config import ScreenConfig
from DataClasses.Config.ScreenConfig import StaffConfig
from DataClasses.ControlData import ControlType
from Helpers.ScreeHelper import ScreenHelper
from Model.Control import Control
from Model.Geometry.Position import Position
from Model.Score.Helpers.StaffUtils import StaffUtils
from DataClasses.Config.MusicConfig import  supported_modulations

class KeySignature(Control):

    def __init__(self, signature_code, name, parent_staff, clef_settings, font_color=(0,0,0)):
        self.key = signature_code
        self.font_color = font_color
        self.signature_patterns =clef_settings["signature_position_pattern"]
        self.signature_details = self.signature_patterns[signature_code]
        _, modulation_details = StaffUtils \
            .find_key_signature_modulation(signature_code, supported_modulations)   
     
        self.modulation_font_code = modulation_details["font_code"]
        self.modulation_font_size =  modulation_details["font_size"]
        self.reference_position = Position.convert_from_tuple(parent_staff.rect.topleft) # this needs to be set.
        self.bounding_box = [self.reference_position.x, self.reference_position.y, 0, 0] # will be set after drawing
        rect = pygame.Rect(400, 400, 40, 40)
        super().__init__(rect, control_type=ControlType.STAFF_ITEM, name=name, 
                                     parent=parent_staff) 

    def set_reference_position(self, position):
        self.reference_position = position

    def get_reference_position(self):
        return self.reference_position
    
    def draw(self, scrollable_screen): 

        modulation_item_index = 1       
        offset_y = self.parent.staff_renderer.vertical_offset # this is to adjust the scroll position.

        for pattern in self.signature_details:
            signature_item_positioning = next(iter(pattern.values()))
            staff_item_type = signature_item_positioning[0] # line/interval
            staff_item_position = None

            if staff_item_type == StaffConfig.STAFF_ITEM_LINE: # line
                staff_item_position = StaffUtils.get_signature_item_coordinates_for_line(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
                                                                 self.modulation_font_size, self.parent.lines, 
                                                                 signature_item_positioning[1], 
                                                                StaffConfig.MODULATION_SPACING, self.reference_position.x)
            elif staff_item_type == StaffConfig.STAFF_ITEM_INTERVAL: # interval
                staff_item_position = StaffUtils.get_signature_item_coordinates_for_interval(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
                                                                                   self.modulation_font_size, self.parent.lines,
                                                                                   self.parent.intervals, signature_item_positioning[1], 
                                                                                   StaffConfig.MODULATION_SPACING, self.reference_position.x)

            signature_position = (staff_item_position.x, staff_item_position.y - offset_y)
            self.draw_modulation(scrollable_screen, self.modulation_font_code, StaffConfig.STAFF_MODULATION_FONT_SIZE,
                                 signature_position)
            
            modulation_item_index += 1           
            self.bounding_box[2] = staff_item_position.x
            self.bounding_box[3] = staff_item_position.y                    
          
        return self.bounding_box

    def draw_modulation(self, screen, modulation_font_code, modulation_font_size, position, modulation_color=(0, 0, 0)):
            modulation_font = ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, modulation_font_size))
            modulation = modulation_font.render(modulation_font_code, True, modulation_color)
            # Get clef rect to position it
            modulation_rect = modulation.get_rect()
            modulation_rect.center = position
            screen.blit(modulation, modulation_rect)