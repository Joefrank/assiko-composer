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

    def render_score(self, screen, music_score):
        # render all staves in Score
        for staff in music_score.staves_sequence:
            if  isinstance(staff, GrandStaff):
                self.staff_renderer.render_grand_staff(staff, screen)
            elif isinstance(staff, Staff):
                self.staff_renderer.render_staff(staff, screen)
        # render credit and title
        self.render_score_credit(screen, music_score)
        self.render_score_title(music_score.title, music_score.title_position, music_score.score_width, screen)
      
    
    def render_score_credit(self, screen, score):
        score_credit = score.credits        
        for credit in score_credit:             
            self.draw_text(screen, credit.text, credit.position, credit.font_size, text_alignment=credit.text_alignment)
                
    
    def render_score_title(self, title, position, container_width, screen):
        font_size = 40
        self.draw_text(screen, title, position, font_size, container_width, text_alignment="CENTER")