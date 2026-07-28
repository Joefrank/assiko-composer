

from DataClasses.Config import ScreenConfig
from DataClasses.ControlData import ControlType
from Helpers.ScreeHelper import ScreenHelper
from Model.Control import Control
from Model.Score.Helpers.StaffUtils import StaffUtils


class Clef(Control):

    def __init__(self, clef_type, name, parent_staff, settings, font_color=(0,0,0)):        
        self.settings = settings
        self.clef_type = clef_type
        self.font_size = settings["size"]
        self.font_color = font_color
        self.font_code = settings["font_code"]
        self.margins = settings["margins"]
        rect = self.get_renderer().get_rect()

        super().__init__(rect, control_type=ControlType.STAFF_ITEM, name=name, 
                                 parent=parent_staff) 

    def get_margins(self):
        return self.margins
    
    def get_renderer(self):
        clef_font_size =ScreenHelper.create_font((ScreenConfig.FontConfig.BRAVURA_FONT_PATH, self.font_size)) 
        return clef_font_size.render(self.font_code, True, self.font_color)

    def move_y(self, offset_y):
        self.rect.y += offset_y
        print(f'moving cleff:{self.rect.y}')

    def move(self, _, offset_y):
       self.move_y(offset_y)
       print(f'moving cleffxxxx:{self.rect.y}')

    def draw(self, scrollable_screen): 

        clef_position = StaffUtils.resolve_position_with_margins(self.parent.rect.topleft, 
                                                                 self.margins)     
        clef_font = self.get_renderer()
        clef_rect = clef_font.get_rect()
        clef_rect.center = (clef_position.x, clef_position.y)
        scrollable_screen.blit(clef_font, clef_rect)

