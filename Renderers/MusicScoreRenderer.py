from datetime import datetime

from Model.Score.GrandStaff import GrandStaff
from Model.Score.Staff import Staff
from Renderers.BaseRenderer import BaseRenderer
from Renderers.StaffRenderer import StaffRenderer


class MusicScoreRenderer(BaseRenderer):

    def __init__(self, state):
        super().__init__(state) 
        self.start_time = datetime.now().time()
        self.staff_renderer = StaffRenderer(state)

    def render_score(self, music_score):
        # render all staves in Score
        original_active_screen = self.staff_renderer.screen
        original_vertical_offset = self.staff_renderer.vertical_offset
        self.staff_renderer.screen = music_score.screen
        self.staff_renderer.vertical_offset = 0 if music_score.parent_container is None else getattr(music_score.parent_container, "scroll_y", 0)
        try:
            
            for staff in music_score.staves_sequence:
                if  isinstance(staff, GrandStaff):
                    self.staff_renderer.render_grand_staff(staff, music_score.screen)
                elif isinstance(staff, Staff):
                    self.staff_renderer.render_staff(staff)
            # render credit
            if music_score.credits:
                self.render_score_credit(music_score.screen, music_score)

            self.render_score_text_inputs(music_score)
            
            #if music_score.title:
                #self.render_score_title(music_score.title, music_score.title_position, music_score.score_width, music_score.screen)
        finally:
            self.staff_renderer.screen = original_active_screen
            self.staff_renderer.vertical_offset = original_vertical_offset
      
    
    def render_score_credit(self, screen, score):
        score_credit = score.credits        
        for credit in score_credit:             
            self.draw_text(screen, credit.text, credit.position, credit.font_size, text_alignment=credit.text_alignment)
                
    
    def render_score_title(self, title, position, container_width, screen):
        font_size = 40
        self.draw_text(screen, title, position, font_size, container_width, text_alignment="CENTER")

    def render_score_text_inputs(self, music_score):
        inputs = music_score.get_text_inputs()
        for text_input in inputs:
            text_input.draw()