

from cmath import rect

import pygame

from DataClasses.ControlData import ControlType
from Model.Containers.ScorePage import ScorePage
from Model.Control import Control
from Model.DragAndDrop.TextItem import TextItem


class ScrollableDocumentViewport(Control):

    def __init__(self, rect, screen, app_state, music_score, no_of_pages=1):       
        super().__init__(rect, ControlType.CONTAINER, "Score Scrollable Document Viewport")
        self.viewport: pygame.Rect = rect
        self.screen = screen
        self.app_state = app_state
        self.music_score = music_score

        self.scroll_y = 0

        self.page_width = rect.width * 0.8
        self.page_height = 1100
        self.page_gap = 80

        #self.pages = []
        self.font = pygame.font.SysFont("segoeui", 20, bold=True)
        self.no_of_pages = no_of_pages
        
        # =====================================================
        # DRAG STATE
        # =====================================================

        self.drag_item = None
        self.drag_page = None

        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.drag_doc_x = 0
        self.drag_doc_y = 0

        self.original_x = 0
        self.original_y = 0

        #self.original_page = None

        # -----------------------------------------
        # Create pages centered in document space
        # -----------------------------------------

        page_x = (self.rect.width - self.page_width) // 2
        y = 100

        for i in range(self.no_of_pages):            
            page_rect = pygame.Rect(page_x, y, self.page_width, self.page_height)
            # Children are pages in the document.
            self.children.append(ScorePage(page_rect, i + 1, screen, self.font, self))
            y += self.page_height + self.page_gap

        self.content_width = self.rect.width

        self.content_height = (
            self.children[-1].rect.bottom
            + 150
        )

        page1 = self.children[0]

        page1.children.append(
            TextItem(pygame.Rect(page1.rect.x + 50, page1.rect.y + 50, 160, 50), "Button 1", screen, self)
        )

        page1.children.append(
            TextItem(pygame.Rect(page1.rect.x + 50, page1.rect.y + 150, 160, 50), "Button 1", screen, self)
        )
        page2 = self.children[1]
        page2.children.append(
            TextItem(pygame.Rect(page2.rect.x + 50, page2.rect.y + 50, 160, 50), "Button 2", screen, self)
        )
              
    # ------------------------------------------------

    def scroll(self, amount):

        max_scroll = max(
            0,
            self.content_height
            - self.viewport.height
        )

        self.scroll_y += amount

        self.scroll_y = max(
            0,
            min(
                max_scroll,
                self.scroll_y
            )
        )

    # ------------------------------------------------

    def draw_scrollbar(self, screen):

        if (
            self.content_height
            <= self.viewport.height
        ):
            return

        ratio = (
            self.viewport.height
            / self.content_height
        )

        bar_height = max(
            40,
            int(
                self.viewport.height
                * ratio
            )
        )

        max_scroll = (
            self.content_height
            - self.viewport.height
        )

        travel = (
            self.viewport.height
            - bar_height
        )

        bar_y = (
            self.viewport.y
            + int(
                travel
                * (
                    self.scroll_y
                    / max_scroll
                )
            )
        )

        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (
                self.viewport.right - 12,
                bar_y,
                10,
                bar_height
            ),
            border_radius=5
        )

    # ------------------------------------------------

    def draw(self):

        # -----------------------------------------
        # Create viewport surface
        # -----------------------------------------

        surface = pygame.Surface(
            self.viewport.size
        )

        # Workspace background
        surface.fill(
            (185, 185, 185)
        )

        # -----------------------------------------
        # Draw pages
        # -----------------------------------------

        for _, page in enumerate(self.children):
           page.draw(surface)

        score_renderer = self.music_score.get_renderer()
        if score_renderer is not None:
            previous_music_score_screen = self.music_score.screen
            self.music_score.set_screen(surface)
            try:
                self.music_score.draw()
            finally:
                self.music_score.set_screen(previous_music_score_screen)


        # -----------------------------------------
        # Clip drawing to viewport
        # -----------------------------------------

        old_clip = self.screen.get_clip()

        self.screen.set_clip(
            self.viewport
        )

        self.screen.blit(
            surface,
            self.viewport.topleft
        )

        self.screen.set_clip(old_clip)

        # Border

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            self.viewport,
            2
        )

        self.draw_scrollbar(self.screen)

    def get_page_at(self, content_pos):
        x, y = content_pos

        for page in self.children:

            if page.rect.collidepoint(x, y):
                return page

        return self.drag_page

    # -----------------------------------------
    # Events Handlers
    # -----------------------------------------
    def on_mouse_wheel(self, event):
        if self.viewport.collidepoint(
                pygame.mouse.get_pos()
            ):

            self.scroll(
                -event.y * 60
            )
    
    def on_mouse_motion(self, event):
         if self.drag_item:

            doc_x, doc_y = self.get_coordinates_in_viewport(event.pos)

            # calculate new coordinates based on offset between mouse position and topleft of the dragged item
            self.drag_doc_x = (doc_x - self.drag_offset_x)
            self.drag_doc_y = (doc_y - self.drag_offset_y)

            self.drag_item.rect.x = self.drag_doc_x            
            self.drag_item.rect.y = self.drag_doc_y
            

    def on_left_mouse_down(self, event):
        
        # Convert to document coordinates
        doc_x, doc_y = self.get_coordinates_in_viewport(event.pos)
       
        self.drag_item = None
        self.drag_page = None
      
        # Search pages/items top-to-bottom        
        for page in reversed(self.children):          
            for item in reversed(page.children):               
                if item.rect.collidepoint(doc_x, doc_y):

                    self.drag_item = item
                    self.drag_page = page

                    # At first click, store original position as that of item.rect.
                    self.drag_doc_x = self.drag_original_x = item.rect.x
                    self.drag_doc_y = self.drag_original_y = item.rect.y
                    # The drag offset is the distance from the mouse position to the top-left corner of the item, in document coordinates. This allows for smooth dragging without the item "jumping" to align with the mouse.
                    self.drag_offset_x = (doc_x - item.rect.x)
                    self.drag_offset_y = (doc_y - item.rect.y)
                 
                    # Bring to front
                    page.children.remove(item)
                    page.children.append(item)

                    break

            if self.drag_item:
                break


    def on_left_mouse_up(self, event):
        # translate mouse position to document coordinates
        doc_x, doc_y = self.get_coordinates_in_viewport(event.pos)
        target_page = self.get_page_at((doc_x, doc_y))

        if self.drag_item: # if item was dragged only within the document viewport.          

            if target_page: # Valid drop target              

                if target_page != self.drag_page:
                    self.drag_page.children.remove(self.drag_item)
                    target_page.children.append(self.drag_item)

            else: # Invalid drop - return to original position
                self.drag_item.rect.x = self.drag_original_x
                self.drag_item.rect.y = self.drag_original_y          

            self.drag_item = None
            self.drag_page = None
        else: # if dragging started from outside of the document viewport.
            self._process_state_change_on_left_mouse_up((doc_x, doc_y), target_page)

    def _process_state_change_on_left_mouse_up(self, drop_coordinates, target_page):      
       dragged_symbol = self.app_state.get_dropped_symbol()
       if dragged_symbol:
           rect, action, params_input = dragged_symbol
           # run the action by calling the function with the parameters
           function = getattr(self.music_score, action, None)
           if function:
               translated_rect = pygame.Rect(
                   drop_coordinates[0],
                   drop_coordinates[1],
                   rect.width,
                   rect.height
               )
               # build a dictionary for other parameters
               input_dict = {"original_value" : params_input, "parent_page": target_page}

               created_item = function(input_dict, translated_rect)
               if created_item:
                    # Now we can directly add the created item to the page based on the drop coordinates.                    
                     if target_page:                         
                          created_item.set_parent(target_page)

           # Now clear the pending dropped symbol from the app state
           self.app_state.clear_dropped_symbol()
       else:
            print("✓ No pending dropped symbol found on mouse up.") 

    def get_coordinates_in_viewport(self, content_pos):      
        return (
             content_pos[0] - self.viewport.x,
             content_pos[1] - self.viewport.y + self.scroll_y
        )