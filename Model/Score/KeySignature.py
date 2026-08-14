
import pygame

from DataClasses.Config.ScreenConfig import StaffConfig
from DataClasses.ControlData import ControlType
from Model.Control import Control
from Model.Score.Helpers.StaffUtils import StaffUtils
from DataClasses.Config.MusicConfig import  supported_modulations

class KeySignature(Control):

    def __init__(self, signature_code, name, parent_staff, clef_settings, font_color=(0,0,0)):
        self.key = None
        signature_patterns =clef_settings["signature_position_pattern"]
        signature_details = signature_patterns[signature_code]
        modulation_name, modulation_details = StaffUtils \
            .find_key_signature_modulation(parent_staff.get_key(), 
                                           supported_modulations)

        # modulation_font_code = modulation_details["font_code"]
        # modulation_font_size =  modulation_details["font_size"]
        # modulation_item_index = 1
        # last_modulation_x_offset = 0 # needed to position next item (time signature)
        
        # for pattern in signature_details:
        #     signature_item_positioning = next(iter(pattern.values()))
        #     staff_item_type = signature_item_positioning[0] # line/interval
        #     staff_item_position = None

        #     if staff_item_type == self.STAFF_ITEM_LINE: # line
        #         staff_item_position = StaffUtils.get_signature_item_coordinates_for_line(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
        #                                                         modulation_font_size, staff.lines, signature_item_positioning[1], 
        #                                                         self.MODULATION_SPACING, reference_position.x)
        #     elif staff_item_type == self.STAFF_ITEM_INTERVAL: # interval
        #         staff_item_position = StaffUtils.get_signature_item_coordinates_for_interval(StaffConfig.STAFF_LINE_GAP, modulation_item_index,
        #                                                                             modulation_font_size, staff.lines,
        #                                                                             staff.intervals, signature_item_positioning[1], self.MODULATION_SPACING, reference_position.x)

        #     signature_position = (staff_item_position.x, staff_item_position.y)
        #     self.draw_modulation(self.screen, modulation_font_code, staff_generic_settings["MODULATION_FONT_SIZE"],
        #                             signature_position)
        #     modulation_item_index += 1
        #     last_modulation_x_offset = staff_item_position.x

        #return 90 if len(signature_details) < 1 else last_modulation_x_offset
        rect = pygame.Rect(400, 400, 40, 40)
        super().__init__(rect, control_type=ControlType.STAFF_ITEM, name=name, 
                                     parent=parent_staff) 