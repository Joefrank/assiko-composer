import pygame
from typing import Any, Callable, List, Optional, Tuple

from DataClasses.ControlData import ControlType
from Model.Control import Control


ItemRenderer = Callable[[pygame.Surface, dict, pygame.Rect, pygame.font.Font, bool], None]


class ScrollableScoreContainer(Control):
    """A scrollable container that can hold and render multiple items."""
    
    def __init__(self, rect: pygame.Rect, screen: pygame.Surface, name: str, score_width: int,            
                 item_height: int = 30,
                 bg_color: Tuple[int, int, int] = (50, 50, 50),
                 border_color: Tuple[int, int, int] = (100, 100, 100),
                 scroll_speed: int = 5,
                 default_renderer: Optional[ItemRenderer] = None):
        super().__init__(rect, ControlType.CONTAINER, name, None)
        """
        Initialize the scrollable container.
        
        Args:
            x: X position of the container
            y: Y position of the container
            width: Width of the container
            height: Height of the container
            item_height: Default height of each item in pixels
            bg_color: Background color (R, G, B)
            border_color: Border color (R, G, B)
            scroll_speed: Pixels to scroll per scroll event
            default_renderer: Optional renderer for items without a custom renderer
        """
       
        self.screen = screen
        self.item_height = item_height
        self.bg_color = bg_color
        self.border_color = border_color
        self.scroll_speed = scroll_speed
        self.default_renderer = default_renderer or self._render_item_default
        
        self.items: List[dict] = []  # List of items with their data and rects
        self.scroll_offset = 0
        self.hovered_item = None
        
        # Create surface for scrollable content
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.surface.fill(bg_color)
        self.font = pygame.font.SysFont(None, 24)
        self.score_width = score_width
    
    def add_item(self, item_id: str, content: Any, data: Optional[dict] = None,
                 renderer: Optional[ItemRenderer] = None,
                 item_height: Optional[int] = None,
                 bg_color: Optional[Tuple[int, int, int]] = None,
                 hover_color: Tuple[int, int, int] = (100, 100, 150),
                 text_color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Add an item to the container.
        
        Args:
            item_id: Unique identifier for the item
            content: Item content (text, surface, object, etc.)
            data: Optional additional data associated with the item
            renderer: Optional custom renderer for this item
            item_height: Optional per-item height in pixels
            bg_color: Background color for this item
            hover_color: Color when item is hovered
            text_color: Default text color if the item renders text
        """
        height = item_height or self.item_height
        start_y = sum(item['height'] for item in self.items)
        item_rect = pygame.Rect(0, start_y, self.rect.width, height)

        item = {
            'id': item_id,
            'content': content,
            'data': data or {},
            'renderer': renderer or self.default_renderer,
            'text_color': text_color,
            'hover_color': hover_color,
            'bg_color': bg_color or self.bg_color,
            'rect': item_rect,
            'height': height
        }
        self.items.append(item)
    
    def remove_item(self, item_id: str) -> bool:
        """
        Remove an item from the container by ID.
        
        Args:
            item_id: The ID of the item to remove
            
        Returns:
            True if item was removed, False if not found
        """
        for i, item in enumerate(self.items):
            if item['id'] == item_id:
                self.items.pop(i)
                self._recalc_item_positions()
                return True
        return False
    
    def clear_items(self):
        """Remove all items from the container."""
        self.items.clear()
        self.scroll_offset = 0
        self.hovered_item = None
    
    def get_item(self, item_id: str) -> Optional[dict]:
        """Get an item by ID."""
        for item in self.items:
            if item['id'] == item_id:
                return item
        return None
    
    def handle_scroll(self, direction: int):
        """
        Handle scrolling.
        
        Args:
            direction: 1 for scroll up, -1 for scroll down
        """
        total_height = sum(item['height'] for item in self.items)
        max_scroll = max(0, total_height - self.height)
        
        self.scroll_offset -= direction * self.scroll_speed
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
    
    def get_item_at_position(self, x: int, y: int) -> Optional[str]:
        """
        Get the item ID at the given screen position.
        
        Args:
            x: Screen X coordinate
            y: Screen Y coordinate
            
        Returns:
            Item ID if found, None otherwise
        """
        if not self.rect.collidepoint(x, y):
            return None
        
        local_y = y - self.y + self.scroll_offset
        for item in self.items:
            if item['rect'].y <= local_y < item['rect'].y + item['height']:
                return item['id']
        return None
    
    def update(self, mouse_pos: Tuple[int, int]):
        """
        Update container state (e.g., hover effects).
        
        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.hovered_item = self.get_item_at_position(mouse_pos[0], mouse_pos[1])
    
    def draw(self):#, surface: pygame.Surface, font: pygame.font.Font):
        """
        Draw the scrollable container on the given surface.
        
        Args:
            surface: Pygame surface to draw on
            font: Font to use for rendering text
        """
        # Draw background and border
        #pygame.draw.rect(self.screen, self.bg_color, self.rect)
       # pygame.draw.rect(self.screen, self.border_color, self.rect, 2)
        
        # Draw score box
        #score_x = self.rect.x + ((self.score_width - self.score_width) // 2)
        #score_box_rect = pygame.Rect(score_x, self.rect.y + 10, self.score_width, self.rect.height - 20)
        #pygame.draw.rect(self.screen, (250, 250, 250), score_box_rect)
       # pygame.draw.rect(self.screen, (255,100,100), score_box_rect, 2)

        # Create a clipping area for the scrollable content
        # clip_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        original_clip = self.screen.get_clip()
        # self.screen.set_clip(clip_rect)
        
        # Draw items
        for item in self.items:
            item_y = self.rect.y + item['rect'].y - self.scroll_offset
            
            if item_y + item['height'] < self.rect.y or item_y > self.rect.y + self.rect.height:
                continue
            
            item_rect = pygame.Rect(self.rect.x, item_y, self.rect.width, item['height'])
            hovered = item['id'] == self.hovered_item
            
            # Draw item background and content using renderer
            item['renderer'](self.screen, item, item_rect, self.font, hovered)
        
        # Restore clipping
        self.screen.set_clip(original_clip)
        
        # Draw scrollbar if needed
        self._draw_scrollbar(self.screen)
    
    def _recalc_item_positions(self):
        """Recalculate the Y-position of every item after a change."""
        offset = 0
        for item in self.items:
            item['rect'].y = offset
            offset += item['height']
    
    def _render_item_default(self, surface: pygame.Surface, item: dict,
                             rect: pygame.Rect, font: pygame.font.Font, hovered: bool):
        """Default rendering for an item."""
        bg_color = item['hover_color'] if hovered else item['bg_color']
        pygame.draw.rect(surface, bg_color, rect)
        pygame.draw.line(surface, self.border_color,
                         (rect.x, rect.y + rect.height),
                         (rect.x + rect.width, rect.y + rect.height), 1)

        content = item['content']
        if isinstance(content, pygame.Surface):
            content_rect = content.get_rect(center=rect.center)
            surface.blit(content, content_rect)
            return

        if isinstance(content, str):
            text_surface = font.render(content, True, item['text_color'])
            text_rect = text_surface.get_rect(topleft=(rect.x + 10, rect.y + 5))
            surface.blit(text_surface, text_rect)
            return

        if hasattr(content, 'draw') and callable(getattr(content, 'draw')):
            content.draw(surface, rect)
            return

        # Fallback: render string representation
        text_surface = font.render(str(content), True, item['text_color'])
        text_rect = text_surface.get_rect(topleft=(rect.x + 10, rect.y + 5))
        surface.blit(text_surface, text_rect)
    
    def _draw_scrollbar(self, surface: pygame.Surface):
        """Draw a scrollbar if content exceeds container height."""
        total_height = sum(item['height'] for item in self.items)
        
        if total_height <= self.rect.height:
            return
        
        scrollbar_width = 10
        scrollbar_height = max(20, int((self.rect.height / total_height) * self.rect.height))
        scrollbar_x = self.rect.x + self.rect.width - scrollbar_width
        scrollbar_y = self.rect.y + int((self.scroll_offset / total_height) * self.rect.height)
        
        scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
        pygame.draw.rect(surface, (150, 150, 150), scrollbar_rect)
        pygame.draw.rect(surface, (100, 100, 100), scrollbar_rect, 1)
