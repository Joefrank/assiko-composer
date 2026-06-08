import pygame

from DataClasses.ControlData import ControlType
from Model.Control import Control


class ScrollableScoreContainer(Control):

    def __init__(
        self,
        viewport_rect,
        content_width,
        content_height,
        page_width,
        page_height,
        screen
    ):
        super().__init__(pygame.Rect(viewport_rect), ControlType.CONTAINER, "ScrollableScoreContainer")

        self.viewport_rect = pygame.Rect(
            viewport_rect
        )

        self.content_width = content_width
        self.content_height = content_height

        self.scroll_x = 0
        self.scroll_y = 0

        # --------------------------------------------------
        # Center page in workspace
        # --------------------------------------------------

        page_x = (
            content_width - page_width
        ) // 2

        page_y = (
            content_height - page_height
        ) // 2

        self.page_rect = pygame.Rect(
            page_x,
            page_y,
            page_width,
            page_height
        )

        self.items = []
        self.screen = screen
        self.drag_item = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    # ------------------------------------------------------

    def center_view_on_page(self):

        self.scroll_x = (
            self.page_rect.centerx
            - self.viewport_rect.width // 2
        )

        self.scroll_y = (
            self.page_rect.centery
            - self.viewport_rect.height // 2
        )

        max_scroll_x = max(
            0,
            self.content_width
            - self.viewport_rect.width
        )

        max_scroll_y = max(
            0,
            self.content_height
            - self.viewport_rect.height
        )

        self.scroll_x = max(
            0,
            min(self.scroll_x, max_scroll_x)
        )

        self.scroll_y = max(
            0,
            min(self.scroll_y, max_scroll_y)
        )

    # ------------------------------------------------------

    def add_item(self, item):
        self.items.append(item)

    # ------------------------------------------------------

    def inside_viewport(self, pos):
        return self.viewport_rect.collidepoint(pos)

    # ------------------------------------------------------

    def screen_to_content(self, pos):

        return (
            pos[0]
            - self.viewport_rect.x
            + self.scroll_x,

            pos[1]
            - self.viewport_rect.y
            + self.scroll_y
        )

    # ------------------------------------------------------

    def scroll(self, dx, dy):

        max_scroll_x = max(
            0,
            self.content_width
            - self.viewport_rect.width
        )

        max_scroll_y = max(
            0,
            self.content_height
            - self.viewport_rect.height
        )

        self.scroll_x += dx
        self.scroll_y += dy

        self.scroll_x = max(
            0,
            min(self.scroll_x, max_scroll_x)
        )

        self.scroll_y = max(
            0,
            min(self.scroll_y, max_scroll_y)
        )

    # ------------------------------------------------------

    def get_item_at(self, mouse_pos):
        print(f"get_item_at called with mouse_pos: {mouse_pos}")
        if not self.inside_viewport(mouse_pos):
            return None
        print("Mouse is inside viewport, checking items...")
        cx, cy = self.screen_to_content(
            mouse_pos
        )

        for item in reversed(self.items):

            if item.rect.collidepoint(cx, cy):
                return item

        print("No item found at the specified position.")
        return None

    # ------------------------------------------------------

    def draw_scrollbars(self, screen):

        # Vertical scrollbar

        if self.content_height > self.viewport_rect.height:

            ratio = (
                self.viewport_rect.height
                / self.content_height
            )

            bar_height = max(
                50,
                int(
                    self.viewport_rect.height
                    * ratio
                )
            )

            max_scroll = (
                self.content_height
                - self.viewport_rect.height
            )

            travel = (
                self.viewport_rect.height
                - bar_height
            )

            bar_y = (
                self.viewport_rect.y
                + int(
                    (self.scroll_y / max_scroll)
                    * travel
                )
            )

            pygame.draw.rect(
                screen,
                (120, 120, 120),
                (
                    self.viewport_rect.right - 12,
                    bar_y,
                    10,
                    bar_height
                ),
                border_radius=4
            )

        # Horizontal scrollbar

        if self.content_width > self.viewport_rect.width:

            ratio = (
                self.viewport_rect.width
                / self.content_width
            )

            bar_width = max(
                50,
                int(
                    self.viewport_rect.width
                    * ratio
                )
            )

            max_scroll = (
                self.content_width
                - self.viewport_rect.width
            )

            travel = (
                self.viewport_rect.width
                - bar_width
            )

            bar_x = (
                self.viewport_rect.x
                + int(
                    (self.scroll_x / max_scroll)
                    * travel
                )
            )

            pygame.draw.rect(
                screen,
                (120, 120, 120),
                (
                    bar_x,
                    self.viewport_rect.bottom - 12,
                    bar_width,
                    10
                ),
                border_radius=4
            )

    # ------------------------------------------------------

    def draw(self):

        viewport_surface = pygame.Surface(
            self.viewport_rect.size
        )

        # Workspace background
        viewport_surface.fill(
            (185, 185, 185)
        )

        # --------------------------------------------------
        # Draw page
        # --------------------------------------------------

        page_screen_rect = self.page_rect.move(
            -self.scroll_x,
            -self.scroll_y
        )

        pygame.draw.rect(
            viewport_surface,
            (255, 255, 255),
            page_screen_rect
        )

        pygame.draw.rect(
            viewport_surface,
            (140, 140, 140),
            page_screen_rect,
            2
        )

        # Page shadow

        shadow_rect = page_screen_rect.move(
            8,
            8
        )

        pygame.draw.rect(
            viewport_surface,
            (160, 160, 160),
            shadow_rect,
            border_radius=4
        )

        pygame.draw.rect(
            viewport_surface,
            (255, 255, 255),
            page_screen_rect
        )

        # --------------------------------------------------
        # Draw items
        # --------------------------------------------------

        for item in self.items:
            item.draw(
                viewport_surface,
                self.scroll_x,
                self.scroll_y
            )

        # --------------------------------------------------
        # Clip drawing
        # --------------------------------------------------

        old_clip = self.screen.get_clip()

        self.screen.set_clip(
            self.viewport_rect
        )

        self.screen.blit(
            viewport_surface,
            self.viewport_rect.topleft
        )

        self.screen.set_clip(old_clip)

        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            self.viewport_rect,
            2
        )

        self.draw_scrollbars(self.screen)


    def on_mouse_wheel(self, event):  
        if self.inside_viewport(
                pygame.mouse.get_pos()
            ):
            mods = pygame.key.get_mods()

        # Shift+Wheel = horizontal scroll
        if mods & pygame.KMOD_SHIFT:
            self.scroll(
                -event.y * 80,
                0
            )
        else:
            self.scroll(
                0,
                -event.y * 80
            )

    def on_mouse_motion(self, event):
        if self.drag_item:
            cx, cy = (
                self.screen_to_content(
                    event.pos
                )
            )

            new_x = (
                cx - self.drag_offset_x
            )

            new_y = (
                cy - self.drag_offset_y
            )

            page = self.page_rect

            # Constrain to page
            new_x = max(
                page.left,
                min(
                    page.right
                    - self.drag_item.rect.width,
                    new_x
                )
            )

            new_y = max(
                page.top,
                min(
                    page.bottom
                    - self.drag_item.rect.height,
                    new_y
                )
            )
            print(f"Dragging item to ({new_x}, {new_y})")
            self.drag_item.rect.x = new_x
            self.drag_item.rect.y = new_y

    def on_left_mouse_down(self, event):
        print(f"get_item_at called with mouse_pos: {event.pos}")
        self.drag_item = self.get_item_at(event.pos)

        if self.drag_item:
            cx, cy = (
                self.screen_to_content(
                    event.pos
                )
            )

            self.drag_offset_x = (
                cx
                - self.drag_item.rect.x
            )

            self.drag_offset_y = (
                cy
                - self.drag_item.rect.y
            )

            # Bring to front
            self.items.remove(
                self.drag_item
            )

            self.items.append(
                self.drag_item
            )

    def on_left_mouse_up(self, event):
        self.drag_item = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
