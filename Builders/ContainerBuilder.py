
import pygame
from DataClasses.MainBoxData import MainBoxConfig
from DataClasses.MainWindowData import MainWindowConfig
from Model.Containers.ScoreContainer import ScoreContainer
from Model.Containers.Window import Window
from Model.Score.MusicScore import MusicScore
from Builders.DynamicStaffBuilder import DynamicStaffBuilder


class ContainerBuilder:

    def  __init__(self, main_window:Window, event_handler):
        self.main_window = main_window
        self.event_handler = event_handler
        self.window_size = main_window.get_size()
        self.height = 0
        self.width = 0
        self.main_box = None

    def build(self):
        return self.build_main_container()

    def build_main_container(self):     
        offset_x = MainWindowConfig.LEFT_PADDING_RATIO *  self.window_size.width
        offset_y = MainBoxConfig.TOP_OFFSET_RATIO * self.window_size.height
        self.height = MainBoxConfig.HEIGHT_RATIO * self.window_size.height
        self.width = MainBoxConfig.WIDTH_RATIO * self.window_size.width        
        music_score = MusicScore(top_left=(offset_x, offset_y), score_width=self.width * 0.9, title="My Music Score", credits="Composed by Me", tempo=120) # Example music score initialization

        self.main_box = ScoreContainer(
            music_score,
            rect=pygame.Rect(offset_x, offset_y, self.width , self.height),
            content_size=(self.width, self.height * 2),
            name=MainBoxConfig.NAME,
            screen=self.main_window.get_canvass(),
            bar_size=MainBoxConfig.BAR_SIZE,
            font_size=MainBoxConfig.FONT_SIZE,
            scroll_speed=MainBoxConfig.SCROLL_SPEED,
            bg_color=MainBoxConfig.BG_COLOR,
            text_color=MainBoxConfig.TEXT_COLOR,
            bar_bg=MainBoxConfig.BAR_BG,
            bar_thumb=MainBoxConfig.BAR_THUMB,
            bar_thumb_hover=MainBoxConfig.BAR_THUMB_HOVER,
            highlight_color=MainBoxConfig.HIGHLIGHT_COLOR,
            container_color=MainBoxConfig.CONTAINER_COLOR,
            enable_x=False,
            enable_y=True
        )
        # Set staff builder. This will build new staffs dynamically when we call CreateStaff method on the music score. 
        music_score.add_child_item_builder("staff", DynamicStaffBuilder(self.main_box))
       
        #register events for mainbox
        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, self.main_box)
        self.event_handler.subscribe(pygame.MOUSEBUTTONUP, self.main_box)
        self.event_handler.subscribe(pygame.MOUSEMOTION, self.main_box)
        self.event_handler.subscribe(pygame.MOUSEWHEEL, self.main_box)
        
        return self.main_box
