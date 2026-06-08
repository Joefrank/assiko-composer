import pygame

from DataClasses.ControlData import ControlType
from Model.Control import Control
from Model.Containers.ScorePage import ScorePage


class ScoreDocument(Control):

    def __init__(self, rect, screen, page_width,  page_height, 
                 page_gap, num_pages, bg_color, page_color, page_border, shadow_color):
        super().__init__(rect, ControlType.CONTAINER, "ScrollableScoreContainer")
        #self.screen_height = screen_height
        #self.screen_width = screen_width
        self.scroll_y = 0
        self.pages = []
        self.bg_color = bg_color
        self.page_color = page_color
        self.page_border = page_border
        self.shadow_color = shadow_color
        self.font = pygame.font.SysFont("segoeui", 20, bold=True)
        self.drag_item = None
        self.drag_page = None
        self.screen = screen
        self.offset_x = 0
        self.offset_y = 0

        page_x = (rect.width - page_width) // 2
        y = rect.y

        for i in range(num_pages):

            rect = pygame.Rect(
                page_x,
                y,
                page_width,
                page_height
            )

            self.pages.append(
                ScorePage(rect, i + 1, screen)
            )

            y += page_height + page_gap

        self.content_height = (
            self.pages[-1].rect.bottom
            + 200
        )

    # -----------------------------------------

    def scroll(self, amount):

        max_scroll = max(
            0,
            self.content_height
            - self.rect.height
        )

        self.scroll_y += amount

        self.scroll_y = max(
            0,
            min(
                max_scroll,
                self.scroll_y
            )
        )

    # -----------------------------------------

    def page_at(self, x, y):

        for page in self.pages:

            if page.rect.collidepoint(x, y):
                return page

        return None

    # -----------------------------------------

    def get_item_at(self, x, y):

        doc_y = y + self.scroll_y

        for page in reversed(self.pages):

            for item in reversed(page.items):

                if item.rect.collidepoint(
                    x,
                    doc_y
                ):
                    return item, page

        return None, None

    # -----------------------------------------

    def draw(self):

        #self.screen.fill(self.bg_color)

        # draw the wrapper rect for pages
        pygame.draw.rect(self.screen, self.bg_color, self.rect)


        for page in self.pages:

            page_screen = page.rect.move(
                0,
                -self.scroll_y
            )

            shadow = page_screen.move(
                8,
                8
            )

            pygame.draw.rect(
                self.screen,
                self.shadow_color,
                shadow
            )

            pygame.draw.rect(
                self.screen,
                self.page_color,
                page_screen
            )

            pygame.draw.rect(
                self.screen,
                self.page_border,
                page_screen,
                1
            )

            # page label

            label = self.font.render(
                f"Page {page.number}",
                True,
                (100, 100, 100)
            )

            self.screen.blit(
                label,
                (
                    page_screen.centerx
                    - label.get_width() // 2,
                    page_screen.bottom - 40
                )
            )

            for item in page.items:
                item.draw(
                    self.screen,
                    self.scroll_y
                )

    # ---------------Event Handlers--------------------------
    def on_left_mouse_down(self, event):

        item, page = (
            self.get_item_at(
                *event.pos
            )
        )

        if item:

            self.drag_item = item
            self.drag_page = page

            doc_y = (
                event.pos[1]
                + self.scroll_y
            )

            self.offset_x = (
                event.pos[0]
                - item.rect.x
            )

            self.offset_y = (
                doc_y
                - item.rect.y
            )

    def on_mouse_motion(self, event):
        if self.drag_item:

            doc_y = (
                event.pos[1]
                + self.scroll_y
            )

            self.drag_item.rect.x = (
                event.pos[0]
                - self.offset_x
            )

            self.drag_item.rect.y = (
                doc_y
                - self.offset_y
            )

    def on_left_mouse_up(self, event):       

        if self.drag_item:

            center_x = (
                self.drag_item.rect.centerx
            )

            center_y = (
                self.drag_item.rect.centery
            )

            target = (
                self.page_at(
                    center_x,
                    center_y
                )
            )

            if (
                target
                and target != self.drag_page
            ):

                self.drag_page.items.remove(
                    self.drag_item
                )

                target.items.append(
                    self.drag_item
                )

            self.drag_item = None
            self.drag_page = None

    def on_mouse_wheel(self, event):

        self.scroll(
            -event.y * 30
        )