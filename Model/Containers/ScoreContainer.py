
import pygame

from Model.Containers.ScrollableContainer import ScrollableContainer


class ScoreContainer(ScrollableContainer):

    def __init__(self, music_score, rect, content_size, name, screen, bar_size, font_size, scroll_speed, bg_color, text_color,
                    bar_bg, bar_thumb, bar_thumb_hover, highlight_color, container_color, enable_x=True, enable_y=True):
        super().__init__(rect, content_size, name, screen, bar_size, font_size, scroll_speed, bg_color, 
                         text_color, bar_bg, bar_thumb, bar_thumb_hover, highlight_color, container_color, enable_x, enable_y)

        self.staves = []  # List of staves, each containing measures and notes
        self.music_score = music_score
        self.score_screen = None
        self.set_music_score_screen(self.content)

    def set_music_score_screen(self, screen: pygame.Surface):
        self.score_screen = screen
        self.music_score.set_screen(screen)

    def get_scrollable_screen(self):
        return self.content
    
    def add_staff(self, staff):
        self.staves.append(staff)

    def on_left_mouse_up(self, event):
       super().on_left_mouse_up(event)
       dragged_symbol = self.app_state.get_dropped_symbol()
       if dragged_symbol:
           rect, action, params_input = dragged_symbol
           # run the action by calling the function with the parameters
           function = getattr(self.music_score, action, None)
           if function:
               function(params_input)

           # Now clear the pending dropped symbol from the app state
           self.app_state.clear_dropped_symbol()
       else:
            print("✓ No pending dropped symbol found on mouse up.") 
   
    def draw(self):
        # Draw music score content into the scrollable surface first,
        # then blit the clipped viewport to the screen.
        self.music_score.draw() # we can use renderers here.
        super().draw()

    
