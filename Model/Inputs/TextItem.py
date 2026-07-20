
import pygame

from DataClasses.ControlData import ControlType
from Model.Score.ScoreControl import ScoreControl


class TextItem(ScoreControl):

    def __init__(self, rect, text, parent_container, 
                 font_size=20, bg_color=(120,190,255), text_color=(20,20,20),
                 border_color=(200,200,200), border_tickness=2):
        super().__init__(rect, control_type=ControlType.TEXT_INPUT, name="TextItem", parent=parent_container)

        self.font = pygame.font.SysFont("segoeui", font_size)
        self.rect = rect
        self.original_text = self.text = text
        self.parent_container = parent_container
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_tickness = border_tickness
        self.border_color = border_color  
        self.active = False
        
        self.cursor_visible = True       
        self.cursor_interval = 500
        self.cursor_pos = 0
        self.padding = 10

    def on_left_mouse_down(self, event):
        actual_pos = self.parent_container.map_coordinates_in_viewport(event.pos)         
        self.active = self.rect.collidepoint(actual_pos)

        if self.active and self.original_text == self.text:
            self.text = ""
        elif not self.active and self.text == "":
            self.text = self.original_text

    def on_key_down(self, event):
        
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            print(f"key: {event.key}")

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

    def draw(self, scrollable_screen=None):
        text_x = self.rect.x + self.padding
        text_y = self.rect.y + (self.rect.height // 2) - (self.font.get_height() // 2)

        if scrollable_screen is None:
            scrollable_screen = self.main_screen

        r = self.rect.move(
            0,
            -self.parent_container.scroll_y
        )

        pygame.draw.rect(
            scrollable_screen,
            self.bg_color,
            r,
            border_radius=2
        )

        pygame.draw.rect(
            scrollable_screen,
            self.border_color,
            r,
            self.border_tickness,
            border_radius=2
        )

        txt = self.font.render(
            self.text,
            True,
            self.text_color
        )

        scrollable_screen.blit(
            txt,
            (
                r.x + 10,
                r.y + 15
            )
        )

        # Cursor ONLY when active
        if self.active and self.cursor_visible:

            cursor_text = self.text[:self.cursor_pos]            
            cursor_x_offset = self.font.size(cursor_text)[0]
            cursor_x = text_x + cursor_x_offset

            pygame.draw.line(
                scrollable_screen,
                self.text_color,
                (cursor_x, text_y),
                (cursor_x, text_y + self.font.get_height()),
                2
            )

    