

import pygame

from DataClasses.ButtonData import ButtonConfig
from Model.Button import Button
from Model.ButtonSymbol import ButtonSymbol
from Model.Position import TextPosition


class StaggeredLabelButton(Button):

    def __init__(self, screen, name, rect, text, action, font, font_details, border_radius=0, 
                 text_position=TextPosition.CENTER, text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
                 bg_color=ButtonConfig.BTN_DEFAULT_COLOR, hover_text_color=ButtonConfig.TEXT_DEFAULT_COLOR, 
                    hover_bg_color=ButtonConfig.BTN_DEFAULT_HOVER, is_draggable=False, icons=[]):
        super().__init__(screen, name, rect, text, action, font, font_details, border_radius, text_position,
                         text_color, bg_color, hover_text_color, hover_bg_color, is_draggable)
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
            button_symbol = ButtonSymbol(label, label_rect, "symbol")           
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