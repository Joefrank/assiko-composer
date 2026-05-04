
import math

from Model.Containers.Window import Window
from Model.Geometry.Position import Position
from Model.Score.MusicScore import MusicScore
from Model.Score.GrandStaff import GrandStaff
from Model.Score.ScoreCredit import ScoreCredit
from Renderers.MusicScoreRenderer import MusicScoreRenderer
from DataClasses.Config.ScreenConfig import ScoreConfig

class MusicScoreBuilder:

    def __init__(self, main_window:Window): 
        self.music_score = None
        self.top_staff = None
        self.highest_credit_y_offset = None 
        self.main_window = main_window
        self.app_state = main_window.get_state()

    """This initializes the score with top staff"""
    def init_score(self, initial_staff, score_title, score_credits, tempo=80):
        if isinstance(initial_staff, GrandStaff):
            self.top_staff = initial_staff.staves[0]
        else: # normal staff            
            self.top_staff = initial_staff
        self.music_score = MusicScore(self.top_staff.top_position, self.top_staff.get_width(), score_title, score_credits, tempo)
        self.music_score.add_staff(initial_staff)
        
        return self

    def build_score_credit(self):
        score_credit = self.music_score.raw_credits
        top_left = self.music_score.top_left_position
        score_width = self.music_score.score_width
        column_width = math.ceil(score_width / len(score_credit))
        no_of_columns = len(score_credit)
        font_size = 20
        self.highest_credit_y_offset = top_left.y # this is used to set title position

        for i in range(no_of_columns):           
            score_credit[i].reverse()
            reversed_array = score_credit[i]
            if i == no_of_columns -1: # align text to right in this case
                text_alignment="RIGHT"
                x_offset = top_left.x + score_width
            else:
                text_alignment="LEFT"
                x_offset = top_left.x + (i * column_width)

            for y in range(len(reversed_array)): 
                position = Position(x_offset, top_left.y - (y * font_size) - 30)  
                if position.y < self.highest_credit_y_offset:
                    self.highest_credit_y_offset = position.y 
                new_credit = ScoreCredit(reversed_array[y], position, text_alignment, font_size)            
                self.music_score.credits.append(new_credit)

        return self
    
    def set_title_position(self):
        top_left = self.music_score.top_left_position
        self.music_score.title_position = Position(top_left.x,  self.highest_credit_y_offset - ScoreConfig.TITLE_Y_OFFSET)
        return self

    def build_blank_score(self, offset_x, offset_y, score_width, score_title="", score_credits=None, tempo=80):
        music_score = MusicScore(top_left=(offset_x, offset_y), score_width=score_width, title=score_title, 
                                 credits=score_credits, tempo=tempo) # Example music score initialization
        music_score.set_state(self.app_state) # pass the state to the music score so that it can access it when needed (e.g. in renderer)
        music_score.title_position = Position(offset_x,  offset_y) # + ScoreConfig.TITLE_Y_OFFSET)
        music_score.set_renderer(MusicScoreRenderer(self.app_state)) # we can add a renderer here to render the score and staves.
       
        return music_score

    def build(self):
        return self.music_score 