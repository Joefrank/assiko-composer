import pygame
import time

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Containers.Container import Container

class ScrollableContainer(Container):
   
    FADE_TIME = 1.0  # seconds

    def __init__(self, rect, content_size, name, screen, bar_size, font_size, scroll_speed, bg_color, text_color,
                    bar_bg, bar_thumb, bar_thumb_hover, highlight_color, container_color, enable_x=True, enable_y=True):
        super().__init__(rect, screen, ControlType.CONTAINER, name, None, bg_color, text_color, 
                         highlight_color, container_color)
        self.content_w, self.content_h = content_size
        self.enable_x = enable_x
        self.enable_y = enable_y
        self.BG_COLOR = bg_color
        self.TEXT_COLOR = text_color
        self.BAR_SIZE = bar_size
        self.font_size = font_size
        self.SCROLL_SPEED = scroll_speed
        self.BAR_BG = bar_bg
        self.BAR_THUMB = bar_thumb
        self.BAR_THUMB_HOVER = bar_thumb_hover

        self.offset_x = 0
        self.offset_y = 0

        self.dragging_content = False
        self.dragging_x = False
        self.dragging_y = False
        self.last_mouse = (0, 0)

        self.last_interaction = 0
        self.hovered = False
        self.is_resizable = True
        
        self.content = pygame.Surface(content_size)
        self.content.fill(self.BG_COLOR)
        self.left_margin = rect[0]
        self.top_margin = rect[1] 
        self.width_percent_of_window = 80
        self.height_percent_of_window = 7 
        self.set_z_index(ControlZIndex.LEVEL1)

    # -----------------------
    # Utility
    # -----------------------
    def clamp(self):
        self.offset_x = max(0, min(self.offset_x, self.content_w - self.rect.width))
        self.offset_y = max(0, min(self.offset_y, self.content_h - self.rect.height))

    def interaction(self):
        self.last_interaction = time.time()

    def scrollbar_alpha(self):
        t = time.time() - self.last_interaction
        if self.hovered:
            return 255
        return max(0, int(255 * (1 - t / self.FADE_TIME)))

    # -----------------------
    # Scrollbar geometry
    # -----------------------
    def vthumb_rect(self):
        ratio = self.rect.height / self.content_h
        h = max(30, self.rect.height * ratio)
        y = self.rect.top + (self.offset_y / self.content_h) * self.rect.height
        return pygame.Rect(
            self.rect.right - self.BAR_SIZE - 2,
            y,
            self.BAR_SIZE,
            h
        )

    def hthumb_rect(self):
        ratio = self.rect.width / self.content_w
        w = max(30, self.rect.width * ratio)
        x = self.rect.left + (self.offset_x / self.content_w) * self.rect.width
        return pygame.Rect(
            x,
            self.rect.bottom - self.BAR_SIZE - 2,
            w,
            self.BAR_SIZE
        )

    # -----------------------
    # Events
    # -----------------------
    def on_left_mouse_down(self, event):
        
        if event.button == 1:
            if self.enable_y and self.vthumb_rect().collidepoint(event.pos):
                self.dragging_y = True
            elif self.enable_x and self.hthumb_rect().collidepoint(event.pos):
                self.dragging_x = True
            elif self.rect.collidepoint(event.pos):
                self.dragging_content = True
            self.last_mouse = event.pos
            self.interaction()

    def on_left_mouse_up(self, event):
        # check if we were dragging a symbol from a button and notify state of drop.
        # if yes, action the current params ans symbols       
        self.dragging_content = self.dragging_x = self.dragging_y = False
        
        
    def on_mouse_motion(self, event):
        self.hovered = self.rect.collidepoint(event.pos)
        if not self.hovered:
            self.interaction()  # Start fade out when mouse leaves
            return

        dx = event.pos[0] - self.last_mouse[0]
        dy = event.pos[1] - self.last_mouse[1]

        if self.dragging_content:
            if self.enable_x:
                self.offset_x -= dx
            if self.enable_y:
                self.offset_y -= dy
            self.interaction()

        if self.dragging_y:
            self.offset_y += dy * (self.content_h / self.rect.height)
            self.interaction()

        if self.dragging_x:
            self.offset_x += dx * (self.content_w / self.rect.width)
            self.interaction()

        self.last_mouse = event.pos
        self.clamp()

    def on_mouse_wheel(self, event):        
            if self.enable_y:
                self.offset_y -= event.y * self.SCROLL_SPEED
            if self.enable_x:
                self.offset_x -= event.x * self.SCROLL_SPEED
            self.interaction()
            self.clamp()
        

    # -----------------------
    # Draw
    # -----------------------
    def draw(self):
        # Clip content cleanly (no border)
        clip = self.screen.get_clip()
        self.screen.set_clip(self.rect)
        self.screen.fill(self.BG_COLOR, self.rect)
        self.screen.blit(
            self.content,
            self.rect.topleft,
            area=pygame.Rect(
                self.offset_x,
                self.offset_y,
                self.rect.width,
                self.rect.height
            )
        )
        
        self.screen.set_clip(clip)

        alpha = self.scrollbar_alpha()
        if alpha <= 0:
            return

        # Scrollbars
        if self.enable_y and self.content_h > self.rect.height:
            thumb = self.vthumb_rect()
            surf = pygame.Surface(thumb.size, pygame.SRCALPHA)
            pygame.draw.rect(
                surf,
                (*self.BAR_THUMB[:3], alpha),
                surf.get_rect(),
                border_radius=6
            )
            self.screen.blit(surf, thumb.topleft)
            #display the scroll position for debugging
            font = pygame.font.SysFont(None, 24)      
            text = font.render(f"Scroll Y: {int(self.offset_y)}", True, (255, 0, 0))
            self.screen.blit(text, (thumb.left - 100, thumb.top))


        if self.enable_x and self.content_w > self.rect.width:
            thumb = self.hthumb_rect()
            surf = pygame.Surface(thumb.size, pygame.SRCALPHA)
            pygame.draw.rect(
                surf,
                (*self.BAR_THUMB[:3], alpha),
                surf.get_rect(),
                border_radius=6
            )
            self.screen.blit(surf, thumb.topleft)

    def add_content(self, text, font_size, text_color, position):
        """Add content to the scrollable area at a specific position."""      
        font = pygame.font.SysFont(None, font_size)
        content = font.render(text, True, text_color)
        self.content.blit(content, position)   

    def resize(self, width_ratio, height_ratio):
        """Resize the visible viewport based on new window size."""
        super().resize_only(width_ratio, height_ratio)
        super().reset_position(width_ratio, height_ratio)
        self.clamp()

    def get_scroll_position(self):
        return self.offset_x, self.offset_y