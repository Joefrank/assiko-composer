import copy

import pygame

from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import ControlZIndex
from Model.Buttons.DialogButton import DialogButton
from Model.Control import Control

class BasicDialog(Control):

    def __init__(self, config, surface, rect, screen, title_font, content_font, parent): # pass button config here , yes_text="Yes", no_text="Cancel"
        super().__init__(rect, ControlType.DIALOG, config.DIALOG_NAME, parent) 
        self.surface = surface
        self.screen = screen  
        self.title_font = title_font 
        self.text_font= content_font    
        self.title = None
        self.message = None
        self.config = config
        self.set_z_index(ControlZIndex.LEVEL4) 
        self.visible = False
        self.result = None  # Store the dialog result
        self.callback = None  # Optional callback function
        parent_size = self.parent.get_size()        
        self.action_buttons = []
        self.target = None

        # Dark transparent background
        self.overlay = pygame.Surface(
            (parent_size.width, parent_size.height),
            pygame.SRCALPHA
        )

        self.overlay.fill((0, 0, 0, 160))        

    def set_buttons(self, buttons):
        self.action_buttons = buttons        
        # remove any action buttons that are already children
        self.children = [child for child in self.children if not isinstance(child, DialogButton)]
        # add the new buttons as children
        for button in buttons:
            self.main_window.get_event_handler().subscribe(pygame.MOUSEBUTTONDOWN, button)
            self.main_window.get_event_handler().subscribe(pygame.MOUSEMOTION, button)          
            self.add_child(button)  # Add button as a child control
       
            
    def add_button(self, button):
        self.children.append(button)  
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width, height):
        self.rect.width = width
        self.rect.height = height
        self.size = (width, height)

    def set_content(self, title, main_content):
        self.title = title
        self.message = main_content   

    def instantiate(self, dialog_config):
        self.set_content(dialog_config.dialog_title, dialog_config.dialog_message)
        self.set_buttons(dialog_config.buttons)  # Assuming buttons are provided in the config
        self.target = dialog_config.target  # Set the target if needed
        self.set_app_state(self.app_state)
        # You can add more configuration settings here as needed

    def close(self):
        """Handle button clicks"""       
        self.visible = False        
        # Call the callback if set 

    def on_left_mouse_down(self, event):
        """Handle mouse clicks on buttons"""
        # Adjust mouse position relative to dialog surface
        relative_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        adjusted_event = pygame.event.Event(event.type, pos=relative_pos)
        
        # Check button clicks
        # if self.yes_button.rect.collidepoint(relative_pos):
        #     self.yes_button.on_left_mouse_down(adjusted_event)
        #     if self.yes_button.action:
        #         self.yes_button.action()
        #     return True
        # elif self.no_button.rect.collidepoint(relative_pos):
        #     self.no_button.on_left_mouse_down(adjusted_event)
        #     if self.no_button.action:
        #         self.no_button.action()
        #     return True
        
        return False

    def on_mouse_motion(self, event):
        """Handle mouse motion for button hover effects"""
        # Adjust mouse position relative to dialog surface
        relative_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        adjusted_event = pygame.event.Event(event.type, pos=relative_pos)
        
        self.yes_button.on_mouse_motion(adjusted_event)
        #self.no_button.on_mouse_motion(adjusted_event)

    def _wrap_text(self, text, max_width):
        if not text:
            return []

        words = text.split()
        if not words:
            return []

        lines = []
        current_line = ""

        for word in words:
            candidate = f"{current_line} {word}".strip()
            if self.text_font.size(candidate)[0] <= max_width:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def draw(self):
        # Draw the dark overlay first (on the main screen)
        self.screen.blit(self.overlay, (0, 0))
        
        # Clear surface with transparency
        self.surface.fill((255, 255, 255, 0))  # Fully transparent
        
        # fill dialog background with rounded corners
        pygame.draw.rect(
            self.surface, 
            self.config.BACKGROUND_COLOR, 
            self.surface.get_rect(),
            border_radius=15  # Adjust radius as needed
        )

        # draw border with rounded corners
        pygame.draw.rect(
            self.surface, 
            self.config.BORDER_COLOR, 
            self.surface.get_rect(), 
            width=3,  # Border thickness
            border_radius=15  # Match the background radius
        )

        # draw title text
        if self.title:
            title_font = self.title_font.render(self.title, True, self.config.TEXT_COLOR)
            self.surface.blit(title_font, (20, 10))

        max_text_width = self.rect.width - 40
        message_y = 70
        line_height = self.text_font.get_height() + 4
        wrapped_lines = self._wrap_text(self.message, max_text_width)

        for line in wrapped_lines:
            if message_y + line_height > self.rect.height - 90:
                break
            message_font = self.text_font.render(line, True, self.config.TEXT_COLOR)
            self.surface.blit(message_font, (20, message_y))
            message_y += line_height

        for child in self.children:
            child.draw()

        # draw dialog onto main screen
        self.screen.blit(self.surface, self.rect)
