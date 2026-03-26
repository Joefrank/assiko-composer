

from DataClasses.ButtonData import ButtonConfig
from Helpers.FileHelper import FileHelper
from Helpers.ScreeHelper import ScreenHelper
from Model.Buttons.Button import Button
from Model.Geometry.Position import TextPosition
import pygame

class ImageButton(Button):

    def __init__(self, config):
        super().__init__(config)
        self.image = None
        self.image_rect = None

    def draw_label(self, text_color):
        self.image, self.image_rect = self.build_image_icon()
        self.screen.blit(self.image, self.image_rect)
        
    def build_image_icon(self):
        asset_path = FileHelper.get_asset_images_paths()
        image_path = asset_path / "Buttons" / f"{self.text}"
        try:
            image = pygame.image.load(str(image_path)).convert_alpha()
            # Scale the image to fit the button rect (90% of rect size)
            scaled_size = (int(self.rect.width * 0.90), int(self.rect.height * 0.90))
            image_item = pygame.transform.scale(image, scaled_size)
            # Center the image in the button
            image_item_rect = image_item.get_rect(center=self.rect.center)
            return image_item, image_item_rect
        except pygame.error:
            print("Error building image icon.build_image_icon()")
       
    def resize(self, new_width_ratio, new_height_ratio):
        # change size of this font        
        self.font_details = (self.font_details[0], int(self.font_details[1] * new_height_ratio))
        self.font = ScreenHelper.create_font(self.font_details)                     
        super().resize_only(new_width_ratio, new_height_ratio)
        # Resize and reposition the image if it exists
        if self.image is not None:
            scaled_size = (int(self.rect.width * 0.90), int(self.rect.height * 0.90))
            self.image = pygame.transform.scale(self.image, scaled_size)
            self.image_rect = self.image.get_rect(center=self.rect.center)
    
    def reposition_children(self, new_width_ratio, new_height_ratio):
        pass
    
    def draw_dragged_icons(self):       
        for dragged_note in self.dragged_symbols: 
            image, image_rect = self.build_image_icon()
            image_rect.center = dragged_note.center
            self.screen.blit(image, image_rect)  

   