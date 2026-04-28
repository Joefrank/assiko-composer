import logging
import pygame
from DataClasses.Config import ScreenConfig
from Model.ApplicationState import ApplicationState
from Renderers import MusicScoreRenderer
from Renderers.BaseRenderer import BaseRenderer


class ScreenRenderer(BaseRenderer):  

    def __init__(self, state:ApplicationState):
        super().__init__(state)
        self.main_canvas = None
        self.logger = logging.getLogger(__name__)
        self.score_renderer = MusicScoreRenderer(state) 
        #self.menu_renderer = MenuRenderer(state)

    def init_screen(self, width, height, caption, background_color=(30, 30, 30)):
        pygame.init()
        self.main_canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.main_canvas.fill(background_color)
        pygame.display.set_caption(caption)
        return self.main_canvas

    def render_frame(self) -> None:
        """Render a complete frame."""
       # try:        
        if (self.state.screen_needs_refresh or self.state.score_navigator.is_running()):
            self._clear_screen(self.state.main_canvass)
            # self.menu_renderer.render_menu()
            self.score_renderer.render_score(self.state.main_canvass, self.state.music_score)               
            pygame.display.flip()
            self.state.set_screen_refresh_status(False)
        #except Exception as e:
           # self.logger.error(f"Rendering error: {e}")

    def _clear_screen(self, screen) -> None:
        """Clear the screen with background color."""
        screen.fill(ScreenConfig.WindowConfig.BACKGROUND_COLOR)