# -----------------------------
# Draggable Symbol
# -----------------------------
import pygame
from Model.DragAndDrop.DraggableControl import DraggableControl


class DraggableSymbolButton(DraggableControl):
    def __init__(self, rect, symbol, font, NOTE_COLOR, NOTE_BG):
        super().__init__(rect)
        self.symbol = symbol
        self.text_surf = font.render(symbol, True, NOTE_COLOR)
        self.note_bg = NOTE_BG
        self.font = font
        self.note_color = NOTE_COLOR
        self.dragged_notes = []
        self.current_dragged_symbol = None

    def draw(self, surface, text_center_position):
        pygame.draw.rect(surface, self.note_bg, self.rect, border_radius=6)
        font = pygame.font.SysFont("Segoe UI Symbol", 26)
        label = font.render(self.symbol, True, (0, 0, 0))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)
        
        # Draw the dragging copy if one exists
        for dragged_note in self.dragged_notes:
            label_copy = font.render(self.symbol, True, (0, 0, 0))
            copy_rect = label_copy.get_rect(center=dragged_note.center)
            surface.blit(label_copy, copy_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                # Create a rect for the dragging copy
                self.current_dragged_symbol = self.rect.copy()
                self.dragged_notes.append(self.current_dragged_symbol)
                # offset keeps the cursor from snapping to top-left
                self.offset = (
                    self.rect.x - event.pos[0],
                    self.rect.y - event.pos[1]
                )

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            if self.current_dragged_symbol in self.dragged_notes:
                self.dragged_notes.remove(self.current_dragged_symbol)
            self.current_dragged_symbol = None
          
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.current_dragged_symbol.x = event.pos[0] + self.offset[0]
            self.current_dragged_symbol.y = event.pos[1] + self.offset[1]