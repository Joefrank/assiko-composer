
import pygame

from DataClasses.Config import ScreenConfig
from DataClasses.ControlData import ControlType
from Helpers.ScreeHelper import ScreenHelper
from Model.Control import Control
from Model.Score.ScoreControl import ScoreControl

"""Class used to input text. When inactive, acts like a label."""
class TextInput(ScoreControl):
    MEDIUM_GRAY = (200, 200, 200)
    LIGHT_GRAY = (240, 240, 240)
    BLUE = (80, 160, 255)
    
    def __init__(self, parent, rect: pygame.Rect, name="TextInput", font_size=20):
        super().__init__(rect, control_type=ControlType.TEXT_INPUT, name=name, parent=parent)

        self.text = ""
        self.text_color = (25, 25, 25)
        self.cursor_pos = 0
        self.font_size = font_size
        self.active = False

        # Cursor blinking
        self.cursor_visible = True       
        self.cursor_interval = 500

        self.padding = 10
        self.parent = parent

    @property
    def position_on_page(self):
        return self.rect.move(
            0,
            -self.parent.scroll_y
        )  
    
    def on_left_mouse_down(self, event):
        actual_pos = (event.pos[0], event.pos[1] - self.parent.scroll_y) 
        print(f"mouse pos:{event.pos} - actual pos: {actual_pos}")
        self.active = self.rect.collidepoint(actual_pos)

    def on_key_down(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = (
                        self.text[:self.cursor_pos - 1]
                        + self.text[self.cursor_pos:]
                    )
                    self.cursor_pos -= 1

            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = (
                        self.text[:self.cursor_pos]
                        + self.text[self.cursor_pos + 1:]
                    )

            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)

            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)

            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0

            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)

            elif event.key == pygame.K_RETURN:
                print("Entered:", self.text)

            else:
                if event.unicode.isprintable():
                    self.text = (
                        self.text[:self.cursor_pos]
                        + event.unicode
                        + self.text[self.cursor_pos:]
                    )
                    self.cursor_pos += 1

            # Reset cursor blink on typing
            self.cursor_visible = True
            #self.cursor_timer = 0

    def on_timer_tick(self, timer):
        self.cursor_visible = not self.cursor_visible

    def draw_boxes(self, scrollable_screen): 
            
        #Draw background box - always visible       
        self.draw_box(scrollable_screen, self.LIGHT_GRAY, border_radius=6, border_width=0)
        # Draw border - only when active
        if self.active:           
            self.draw_box(scrollable_screen, self.BLUE, border_radius=6, border_width=2)  # Blue border when active
        else:
            # Draw subtle border when inactive
            self.draw_box(scrollable_screen, self.MEDIUM_GRAY, border_radius=6, border_width=1)  # Medium gray background                
      
    def draw(self, scrollable_screen):        
        self.draw_boxes(scrollable_screen)
        font = pygame.font.Font(None, self.font_size)
        text_x = self.rect.x + self.padding
        text_y = self.rect.y + (self.rect.height // 2) - (font.get_height() // 2)
        text_surface = font.render(self.text, True, self.text_color)
        scrollable_screen.blit(text_surface, (text_x, text_y))

        # calculate width of text and resize input box accordingly, with a max width limit
        text_width = font.size(self.text)[0]
        if text_width > self.rect.width - 2 * self.padding:
            # check that we are not exceeding the parent container's width
            #print(f"box width:{self.rect.width} - text width: {text_width} - parent score width: {self.parent.score_width}")
            
            new_width = self.rect.width + (2 * self.padding)
            can_extend = self.parent.score_width - (self.rect.x + new_width)
           # print(f"self.rect.x: {self.rect.x} - new_width: {new_width} - parent score width: {self.parent.score_width} - can_extend: {can_extend}")
            if can_extend > 0:
                self.rect.width = new_width
            else:
                self.active = False  # Deactivate input if we exceed parent container width

        # Cursor ONLY when active
        if self.active and self.cursor_visible:

            cursor_text = self.text[:self.cursor_pos]            
            cursor_x_offset = font.size(cursor_text)[0]
            cursor_x = text_x + cursor_x_offset

            pygame.draw.line(
                scrollable_screen,
                self.text_color,
                (cursor_x, text_y),
                (cursor_x, text_y + font.get_height()),
                2
            )

    def draw_box(self, scrollable_screen, color, border_radius=6, border_width=0):
        # Draw background box
        pygame.draw.rect(
            scrollable_screen,
            color,
            self.rect,
            border_width,
            border_radius
        )