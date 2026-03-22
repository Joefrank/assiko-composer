import pygame
from DataClasses.ButtonData import ButtonType
from DataClasses.ControlData import ControlType
from DataClasses.MainWindowData import MainWindowConfig
from DataClasses.ToolbarData import TOOLBAR_MATRIX, NotesToolbar, PlayToolbar, RestToolbar, ToolbarDimensions, ToolbarGridConfig
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Factories.ButtonBuildersFactory import ButtonBuildersFactory
from Helpers.ScreeHelper import ScreenHelper
from Model.Buttons.Button import Button
from Model.Containers.Grid import Grid
from Model.Buttons.StaggeredLabelButton import StaggeredLabelButton
from Model.Toolbars.StaggeredButtonToolbar import StaggeredButtonToolbar
from Model.Toolbars.Toolbar import Toolbar
from Model.Containers.Window import Window

class ToolbarBuilder:

    def __init__(self, main_window:Window, event_handler:MainWindowEventHandler):
        self.window_size = main_window.get_size()
        self.screen = main_window.get_canvass()
        self.event_handler = event_handler
        self.grid_offset_x = MainWindowConfig.LEFT_PADDING_RATIO * self.window_size.width
        self.grid_offset_y = ToolbarDimensions.TOP_OFFSET_RATIO * self.window_size.height
        self.toolbar_height = ToolbarDimensions.TOOLBAR_HEIGHT_RATIO * self.window_size.height
        self.toolbar_item_height = ToolbarDimensions.TOOLBAR_ITEM_HEIGHT_RATIO * self.window_size.height
        self.toolbar_item_width = ToolbarDimensions.TOOLBAR_ITEM_WIDTH_RATIO * self.window_size.width
        self.grid_spacing = ToolbarGridConfig.GRID_SPACING # space between various toolbars.
        self.grid_width = MainWindowConfig.MAIN_CONTAINER_WIDTH_RATIO * self.window_size.width
        self.no_of_grid_rows = len(TOOLBAR_MATRIX)
        self.grid_height = (self.toolbar_height * self.no_of_grid_rows) + self.grid_spacing[1]  
        self.toolbars = []
        self.simple_button_types = [ButtonType.BUTTON, ButtonType.TIME_SIGNATURE_BUTTON, ButtonType.IMAGE_BUTTON]

  
    def build(self):
        # we build a Grid object to hold all our toolbars, this way we can easily manage their layout and resizing together
        toolbar_grid_rect = pygame.Rect(self.grid_offset_x, self.grid_offset_y, self.grid_width, self.grid_height)
        toolbar_grid = Grid(toolbar_grid_rect, self.screen, None, ToolbarGridConfig.GRID_NAME, 
                            show_grid_lines=False, grid_spacing=self.grid_spacing)
        grid_row_sizes = [0] * self.no_of_grid_rows
        
        for i, row in enumerate(TOOLBAR_MATRIX):            
            cumulative_row_width =toolbar_x_offset = self.grid_offset_x
            toolbar_y_offset = self.grid_offset_y + ((self.toolbar_height + self.grid_spacing[1]) * i)
            grid_row_sizes[i] =0
            for j, value in enumerate(row):
                grid_coordinates = (i, j)    
                toolbar_x_offset = cumulative_row_width 
               
                toolbar = self._build_toolbar(value, toolbar_x_offset, toolbar_y_offset, self.toolbar_height,
                                              self.toolbar_item_height, self.toolbar_item_width, 
                                              grid_coordinates, self.grid_spacing)
                cumulative_row_width += toolbar.rect.width + self.grid_spacing[0]                
                toolbar_grid.add_child(toolbar)
                grid_row_sizes[i] += 1
        
        toolbar_grid.set_grid_sizes(grid_row_sizes)
        print(grid_row_sizes)
        return toolbar_grid ### change consuming function to handle grid instead of individual toolbars, we can get individual toolbars from grid's children when needed
        
    """Builds each toolbar based on settings in config."""
    def _build_toolbar(self, spec, offset_x, offset_y, toolbar_height, toolbar_item_height, toolbar_item_width, 
                       grid_coordinates, grid_spacing):
        font = ScreenHelper.create_font(spec.FONT)
        button_type = getattr(spec, 'BUTTON_TYPE', ControlType.BUTTON)
        rect = pygame.Rect(offset_x, offset_y, ToolbarDimensions.DEFAULT_TOOLBAR_WIDTH, toolbar_height)
        if button_type in self.simple_button_types:
            toolbar = Toolbar(rect, self.screen, spec.NAME, toolbar_item_width, toolbar_item_height,
                            ToolbarDimensions.BUTTON_MARGIN, button_text_center=getattr(spec, 'BUTTON_TEXT_CENTER', None),
                            buttons_draggable=getattr(spec, 'DRAGGABLE_BUTTONS', False),
                            grid_coordinates=grid_coordinates, grid_spacing=grid_spacing)
        elif button_type == ButtonType.STAGGERED_SYMBOL_BUTTON:
            toolbar = StaggeredButtonToolbar(rect, self.screen, spec.NAME, toolbar_item_width, toolbar_item_height,
                            ToolbarDimensions.BUTTON_MARGIN, button_text_center=getattr(spec, 'BUTTON_TEXT_CENTER', None),
                            buttons_draggable=getattr(spec, 'DRAGGABLE_BUTTONS', False),
                            grid_coordinates=grid_coordinates, grid_spacing=grid_spacing)
      

        toolbar.add_supported_events(spec.SUPPORTED_EVENTS)
       
        buttons = self.setup_buttons(toolbar, spec.ICONS, font, spec.FONT, toolbar_height,
                            getattr(spec, 'BUTTON_TEXT_COLOR', None), getattr(spec, 'BUTTON_BG_COLOR', None),
                            getattr(spec, 'BUTTON_HOVER_TEXT_COLOR', None), getattr(spec, 'BUTTON_HOVER_BG_COLOR', None),
                            ToolbarDimensions.BUTTON_BORDER_RADIUS, button_type)        
        
        if button_type == ButtonType.STAGGERED_SYMBOL_BUTTON:
            toolbar.reset_children_positions()
            
        # register buttons for event handling
        for button in buttons:
            self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, button)
            self.event_handler.subscribe(pygame.MOUSEMOTION, button)
            if toolbar.buttons_draggable:
                self.event_handler.subscribe(pygame.MOUSEBUTTONUP, button)

        return toolbar
    
    """Create buttons for toolbar."""
    def setup_buttons(self, toolbar, icons:list[tuple[str, str]], font, font_details, toolbar_height, # pass height of toolbar here
                    text_color, bg_color, hover_text_color, hover_bg_color, border_radius=0, button_type=ButtonType.BUTTON):
        button_top_padding = (toolbar_height - toolbar.button_height) // 2
        x = ToolbarDimensions.BUTTON_MARGIN  
        button_builder = ButtonBuildersFactory().get_button_builder(button_type)
        buttons =[]  
        for icon, action in icons:
            button = button_builder.build_button(self.screen, toolbar, action, icon, font, font_details, border_radius, text_color,
                             bg_color, hover_text_color, hover_bg_color, toolbar.buttons_draggable, (x,button_top_padding))

            toolbar.add_button(button)
            buttons.append(button)
            x += toolbar.button_width + toolbar.button_margin

        return buttons
    
   