

import pygame

from DataClasses.ButtonData import ButtonConfig
from Model.Buttons.Button import Button
from Model.Buttons.ButtonIcons.ButtonSymbol import ButtonSymbol
from Model.Geometry.Position import TextPosition


class StaggeredLabelButton(Button):

    def __init__(self, config, icons=[]):
        super().__init__(config)
        self.icons = icons
        self.icon_spacing = 4 # used for icons horizontal spacing.
        self.button_padding = 10  
        self.icon_staggered_spacing = 4 # used for symbol vertical spacing.
        self.drawn = True

    def draw(self):
        # display the symbols and button container
        super().draw_button_frame()  
        self.display_symbols()

        #self.drawn = False
      
        if self.is_draggable:
            # Draw the dragging copy if one exists
            ## TODO: work out the dragged icons copy based on currently dragged symbol.
            self.draw_dragged_icons()

    def build_staggered_symbols(self) -> int:        
        symbols_total_width = self.button_padding
        start_x = self.rect.x + self.button_padding
        start_y = self.rect.centery
        # clear existing drawn symbols
        self.children.clear()

        # Loop through the symbols and render each one spacing them evenly like a zigzag pattern. up and down.
        for i, symbol in enumerate(self.icons):
            label = self.font.render(symbol, True, self.text_color)
            label_rect = label.get_rect()
            symbol_width = label_rect.width + self.icon_spacing
            x = start_x + (i * symbol_width)
            y = start_y + ((i % 2) * self.icon_staggered_spacing)
            label_rect.center = (x, y)  # 5 pixels gap between symbols 
            button_symbol = ButtonSymbol(label, label_rect, "symbol", symbol)           
            self.add_child(button_symbol)
            symbols_total_width += symbol_width
            
        return symbols_total_width
    
    def display_symbols(self):
        # check that array of drawn symbols is not empty
        if len(self.children) == 0:
            return
        for item in self.children:
            self.screen.blit(item.label, item.rect)

    def reset_children_positions(self, x_difference):       
        for child in self.children:
            child.move_horizontally(x_difference)

    def resize(self, new_width_ratio, new_height_ratio):
        # Resize the button rect first
        super().resize_only(new_width_ratio, new_height_ratio)

    def move_children(self, h_move, v_move):
        for child in self.children:
            child.move(h_move, v_move)

    def draw_dragged_icons(self):       
        for dragged_note in self.dragged_symbols:           
            for child in self.children:
                x_offset = child.rect.x - self.rect.x
                y_offset = child.rect.y - self.rect.y
                label_copy = self.font.render(child.symbol, True, (0, 0, 0))
                copy_rect = label_copy.get_rect()
                copy_rect.center = (dragged_note.x + x_offset, dragged_note.y + y_offset)
                self.screen.blit(label_copy, copy_rect)    
