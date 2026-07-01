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

        # Dark transparent background
        self.overlay = pygame.Surface(
            (parent_size.width, parent_size.height),
            pygame.SRCALPHA
        )

        self.overlay.fill((0, 0, 0, 160))

        # Use relative position within the surface (not absolute screen position)
        self.button_y = self.rect.height - 70  # Changed from self.rect.bottom
    
        # self.yes_button = DialogButton(
        #     pygame.Rect(
        #         self.rect.width // 2 - 140,
        #         self.button_y,
        #         110,
        #         45
        #     ),
        #     "Yes",
        #     self.text_font,
        #     self.surface,
        #     "Yes button",
        #     (50, 170, 80)
        # )

        # # Set action for Yes button
        # self.yes_button.set_action(lambda: self.on_button_click("yes"))
        # self.yes_button.subscribe_to_event(pygame.MOUSEBUTTONDOWN)
        # self.yes_button.subscribe_to_event(pygame.MOUSEMOTION)

        # self.no_button = DialogButton(
        #      pygame.Rect(
        #         self.rect.width // 2 + 30,
        #         self.button_y,
        #         110,
        #         45
        #     ),
        #     "No",
        #     self.text_font,
        #     self.surface,
        #     "No button",
        #     (190, 70, 70)
        # )
        # # Set action for No button
        # self.no_button.set_action(lambda: self.on_button_click("no"))

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

    def clone(self):
        dialog_copy = copy.deepcopy(self)
        dialog_copy.name += "-copy" 
        return dialog_copy
    
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

    def set_callback(self, callback):
        """Set a callback function to be called when a button is clicked"""
        self.callback = callback

    def on_button_click(self, value):
        """Handle button clicks"""
        self.result = value
        self.visible = False
        print("click called.")
        
        # Call the callback if set
        if self.callback:
            self.callback(value)
        
        return value

    def get_result(self):
        """Get the dialog result"""
        return self.result

    def show(self):
        """Show the dialog and reset result"""
        self.result = None
        self.visible = True

    def on_left_mouse_down(self, event):
        """Handle mouse clicks on buttons"""
        # Adjust mouse position relative to dialog surface
        relative_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        adjusted_event = pygame.event.Event(event.type, pos=relative_pos)
        
        # Check button clicks
        if self.yes_button.rect.collidepoint(relative_pos):
            self.yes_button.on_left_mouse_down(adjusted_event)
            if self.yes_button.action:
                self.yes_button.action()
            return True
        elif self.no_button.rect.collidepoint(relative_pos):
            self.no_button.on_left_mouse_down(adjusted_event)
            if self.no_button.action:
                self.no_button.action()
            return True
        
        return False

    def on_mouse_motion(self, event):
        """Handle mouse motion for button hover effects"""
        # Adjust mouse position relative to dialog surface
        relative_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        adjusted_event = pygame.event.Event(event.type, pos=relative_pos)
        
        self.yes_button.on_mouse_motion(adjusted_event)
        self.no_button.on_mouse_motion(adjusted_event)

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
        title_font = self.title_font.render(self.title, True, self.config.TEXT_COLOR)
        self.surface.blit(title_font, (20, 10))

        for child in self.children:
            child.draw()

        # draw message text
        message_font = self.text_font.render(self.message, True, self.config.TEXT_COLOR)
        self.surface.blit(message_font, (20, (self.rect.height // 3) - 10))

        # draw dialog onto main screen
        self.screen.blit(self.surface, self.rect)
