
import pygame
from Builders.MusicScoreBuilder import MusicScoreBuilder
from DataClasses.Config.ScreenConfig import ScoreConfig
from DataClasses.MainBoxData import MainBoxConfig
from DataClasses.MainWindowData import MainWindowConfig
from Model.Containers.ScoreDocument import ScoreDocument
from Model.Containers.ScrollableDocumentViewPort import ScrollableDocumentViewport
from Model.Containers.ScrollableScoreContainer import ScrollableScoreContainer
from Model.Containers.ScoreContainer import ScoreContainer
from Model.Containers.Window import Window
from Builders.DynamicStaffBuilder import DynamicStaffBuilder
from Model.DragAndDrop.DraggableItem import DraggableItem
from Model.DragAndDrop.TextItem import TextItem


class ContainerBuilder:

    def  __init__(self, main_window:Window, event_handler):
        self.main_window = main_window
        self.event_handler = event_handler
        self.window_size = main_window.get_size()
        self.height = 0
        self.width = 0
        self.main_box = None
        self.score_builder = MusicScoreBuilder(main_window)

    def build(self):
        return self.build_score_container()

    def build_score_container(self):     
        offset_x = int(MainWindowConfig.LEFT_PADDING_RATIO *  self.window_size.width)
        offset_y = int(MainBoxConfig.TOP_OFFSET_RATIO * self.window_size.height)
        self.height = int(MainBoxConfig.HEIGHT_RATIO * self.window_size.height)
        self.width = int(MainBoxConfig.WIDTH_RATIO * self.window_size.width)        
        score_width = int(self.width * MainBoxConfig.SCORE_WIDTH_RATIO)
        rect = pygame.Rect(offset_x, offset_y, self.width, self.height)

        """The score coordinates start from offset (0,0) based on the mainbox because this is a scrollable container."""
        music_score = self.score_builder.build_blank_score(
            0,
            0,
            score_width=score_width,
            score_title="....Title Here....",
            score_credits="Composed by Me",
            tempo=120
        )
        
        # Set staff builder. This will build new staffs dynamically when we call CreateStaff method on the music score. 
        music_score.add_child_item_builder("staff", DynamicStaffBuilder(self.main_window.get_state()))

        score_document = ScrollableDocumentViewport(
            rect,
            self.main_window.get_canvass(),
            self.main_window.get_state(),
            music_score,
            no_of_pages=2
        )

        music_score.set_parent_container(score_document)

       
        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, score_document)
        self.event_handler.subscribe(pygame.MOUSEBUTTONUP, score_document)
        self.event_handler.subscribe(pygame.MOUSEMOTION, score_document)
        self.event_handler.subscribe(pygame.MOUSEWHEEL, score_document)

        return score_document
    
       

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
       
        music_score.set_parent_container(self.main_box)
        
        # Set staff builder. This will build new staffs dynamically when we call CreateStaff method on the music score. 
        music_score.add_child_item_builder("staff", DynamicStaffBuilder(self.main_window.get_state()))

        #register events for mainbox
        self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, self.main_box)
        self.event_handler.subscribe(pygame.MOUSEBUTTONUP, self.main_box)
        self.event_handler.subscribe(pygame.MOUSEMOTION, self.main_box)
        self.event_handler.subscribe(pygame.MOUSEWHEEL, self.main_box)

        return self.main_box
