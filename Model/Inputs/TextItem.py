
import pygame

from DataClasses.ControlData import ControlType
from Model.Score.ScoreControl import ScoreControl


class TextItem(ScoreControl):

    def __init__(self, rect, text, parent_container, 
                 font_size=18, bg_color=(120,190,255), inactive_bg_color=(250,240,250), text_color=(20,20,20),
                 border_color=(200,200,200), border_thickness=2, inactive_border_thickness=1):
        super().__init__(rect, control_type=ControlType.TEXT_INPUT, name="TextItem", parent=parent_container)

        self.font = pygame.font.SysFont("segoeui", font_size)
        self.rect = rect
        self.original_text = self.text = text
        self.parent_container = parent_container
        self.bg_color = bg_color
        self.inactive_bg_color = inactive_bg_color
        self.text_color = text_color
        self.border_thickness = border_thickness
        self.inactive_border_thickness = inactive_border_thickness
        self.border_color = border_color  
        self.active = False
        
        self.cursor_visible = True       
        self.cursor_interval = 500
        self.cursor_pos = 0
        self.padding = 10
        self.last_mouse_pos = None

    @property
    def min_x(self):
        _, leftmost_x_offset  = self.parent_container.get_drawing_boundaries()
        return leftmost_x_offset
    
    @property
    def max_x(self):
        max_width, leftmost_x_offset  = self.parent_container.get_drawing_boundaries()
        return (leftmost_x_offset + max_width)
    
    def adjust_position(self):       
        if self.rect.x < self.min_x:
            self.rect.x = self.min_x
        elif self.rect.x > self.max_x:
            self.rect.x = self.max_x

    def on_left_mouse_down(self, event):
        self.last_mouse_pos = self.parent_container.map_coordinates_in_viewport(event.pos)         
        self.active = self.rect.collidepoint(self.last_mouse_pos)

        if self.active and self.original_text == self.text:
            self.text = ""
        elif not self.active and self.text == "":
            self.text = self.original_text

    def on_key_down(self, event):
        self.last_mouse_pos = None

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
                self.active = False
            else:
                if event.unicode.isprintable():
                    self.process_new_input(
                        self.text[:self.cursor_pos]
                         + event.unicode
                         + self.text[self.cursor_pos:]
                    )                  

            # Reset cursor blink on typing
            self.cursor_visible = True
            #self.cursor_timer = 0

    def on_timer_tick(self, timer):
        self.cursor_visible = not self.cursor_visible

    def process_new_input(self, input_text):
        # calculate width of text and resize input box accordingly, with a max width limit
        text_width = self.font.size(input_text)[0] 
        width_increment = 2 * self.padding        
        text_input_threshold = self.rect.width - (width_increment)
       
        # When the text content exceeds textitem size (width)
        if text_width > text_input_threshold:            
            # check that we are not exceeding the parent container's width
            new_width = self.rect.width + width_increment
            x_diff = self.rect.x - self.min_x
            can_extend = self.max_width > (x_diff + new_width)
            
            if can_extend:
                self.rect.width = new_width
                self.text = input_text                
            elif x_diff > 0:
                self.rect.x -= width_increment
                self.rect.width = new_width
                self.text = input_text            
            else:
                self.active = False  # Deactivate input if we exceed parent container width
        else:
            self.text = input_text

        self.cursor_pos += 1

    def move(self, offset_x:int, offset_y:int):
        new_offset_x =  self.rect.x + offset_x

        if new_offset_x >= self.min_x and (new_offset_x + self.rect.width) < self.max_x:
            self.rect.x += offset_x

        #### Handle vertical move at page level or even score level
        self.rect.y += offset_y

        self.last_mouse_pos = None

    def draw(self, scrollable_screen=None):
        if scrollable_screen is None:
            scrollable_screen = self.main_screen

        r = self.rect.move(0, -self.parent_container.scroll_y)
        text_x = r.x + self.padding
        text_y = r.y + (self.rect.height // 2) - (self.font.get_height() // 2)
        bg_color = self.bg_color if self.active else self.inactive_bg_color
        border_thickness = self.border_thickness if self.active else self.inactive_border_thickness

        pygame.draw.rect(
            scrollable_screen,
            bg_color,
            r,
            border_radius=2
        )

        pygame.draw.rect(
            scrollable_screen,
            self.border_color,
            r,
            border_thickness,
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
                r.y + 10
            )
        )

        if self.active and self.cursor_visible:
            cursor_text = self.text[:self.cursor_pos]
            cursor_x = text_x + self.font.size(cursor_text)[0]
            pygame.draw.line(
                scrollable_screen,
                self.text_color,
                (cursor_x, text_y),
                (cursor_x, text_y + self.font.get_height()),
                2
            )

    