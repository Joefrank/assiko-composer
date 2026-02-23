import pygame
from DataClasses.MainWindowData import MainWindowConfig
from DataClasses.ToolbarData import NotesToolbar, PlayToolbar, RestToolbar, ToolbarDimensions, ToolbarGridConfig
from EventHandlers.MainWindowEventHandler import MainWindowEventHandler
from Model.Grid import Grid
from Model.Toolbars.Toolbar import Toolbar
from Model.Window import Window

class ToolbarBuilder:

    def __init__(self, main_window:Window, event_handler:MainWindowEventHandler):
          self.window_size = main_window.get_size()
          self.screen = main_window.get_canvass()
          self.event_handler = event_handler
          self.toolbars = []

    def build(self):   
        offset_x = MainWindowConfig.LEFT_PADDING_RATIO * self.window_size.width
        offset_y = ToolbarDimensions.TOP_OFFSET_RATIO * self.window_size.height
        toolbar_height = ToolbarDimensions.TOOLBAR_HEIGHT_RATIO * self.window_size.height
        toolbar_item_height = ToolbarDimensions.TOOLBAR_ITEM_HEIGHT_RATIO * self.window_size.height
        toolbar_item_width = ToolbarDimensions.TOOLBAR_ITEM_WIDTH_RATIO * self.window_size.width
        grid_spacing = ToolbarGridConfig.GRID_SPACING
        grid_width = ToolbarDimensions.MAIN_CONTAINER_WIDTH_RATIO * self.window_size.width
        grid_rows = 2  # we assume max 2 rows of toolbars for now, this can be adjusted based on actual number of toolbars and their sizes
        grid_height = (toolbar_height * grid_rows) + grid_spacing[1]  # we assume max 2 rows of toolbars for now, this can be adjusted based on actual number of toolbars and their sizes

        # we build a Grid object to hold all our toolbars, this way we can easily manage their layout and resizing together
        toolbar_grid_rect = pygame.Rect(offset_x, offset_y, grid_width, grid_height)
        toolbar_grid = Grid(toolbar_grid_rect, (ToolbarGridConfig.GRID_ROWS, ToolbarGridConfig.GRID_COLS), 
                            self.screen, None, ToolbarGridConfig.GRID_NAME, show_grid_lines=False, grid_spacing=grid_spacing)
        
        toolbar_specs = [PlayToolbar, NotesToolbar, RestToolbar]
        toolbar_x_offset = offset_x
        toolbar_y_offset = offset_y
        for x in range(ToolbarGridConfig.GRID_COLS):
            for y in range(ToolbarGridConfig.GRID_ROWS):
                grid_coordinates = (x, y)
                # get next spec from toolbar_specs
                spec = toolbar_specs[(y * ToolbarGridConfig.GRID_COLS + x) % len(toolbar_specs)]
                toolbar = self._build_toolbar(spec, toolbar_x_offset, toolbar_y_offset, toolbar_height,
                                          toolbar_item_height, toolbar_item_width, 
                                          grid_coordinates, grid_spacing)
                toolbar_y_offset += y * (toolbar_height + grid_spacing[1])
                toolbar_grid.add_child(toolbar)
                #self.toolbars.append((spec.NAME, toolbar))

        #grid_col = 0
        #for spec in toolbar_specs:
            # grid_coordinates = (grid_col, 0)  # (column, row)
            # toolbar = self._build_toolbar(spec, offset_x, offset_y, toolbar_height,
            #                               toolbar_item_height, toolbar_item_width, 
            #                               grid_coordinates, grid_spacing)
            # self.toolbars.append((spec.NAME, toolbar))
            # offset_x = toolbar.rect.right + grid_spacing[0]
            # grid_col += 1

        return toolbar_grid ### change consuming function to handle grid instead of individual toolbars, we can get individual toolbars from grid's children when needed

    def _build_toolbar(self, spec, offset_x, offset_y, toolbar_height, toolbar_item_height, toolbar_item_width, 
                       grid_coordinates, grid_spacing):
        font = self._create_font(spec.FONT)

        rect = pygame.Rect(offset_x, offset_y, ToolbarDimensions.DEFAULT_TOOLBAR_WIDTH, toolbar_height)
        toolbar = Toolbar(rect, self.screen, spec.NAME, toolbar_item_width, toolbar_item_height,
                          ToolbarDimensions.BUTTON_MARGIN, button_text_center=getattr(spec, 'BUTTON_TEXT_CENTER', None),
                          buttons_draggable=getattr(spec, 'DRAGGABLE_BUTTONS', False),
                          grid_coordinates=grid_coordinates, grid_spacing=grid_spacing)
        toolbar.add_supported_events(spec.SUPPORTED_EVENTS)
        buttons = toolbar.create_buttons(spec.ICONS, font, toolbar_height,
                            getattr(spec, 'BUTTON_TEXT_COLOR', None), getattr(spec, 'BUTTON_BG_COLOR', None),
                            getattr(spec, 'BUTTON_HOVER_TEXT_COLOR', None), getattr(spec, 'BUTTON_HOVER_BG_COLOR', None),
                            ToolbarDimensions.BUTTON_BORDER_RADIUS)
        
       
        # register buttons for event handling
        for button in buttons:
            self.event_handler.subscribe(pygame.MOUSEBUTTONDOWN, button)
            self.event_handler.subscribe(pygame.MOUSEMOTION, button)
            if toolbar.buttons_draggable:
                self.event_handler.subscribe(pygame.MOUSEBUTTONUP, button)

        return toolbar
    
    
    def _create_font(self, font_spec):
        name, size = font_spec
        try:
            return pygame.font.Font(name, size)
        except Exception:
            return pygame.font.SysFont(name if isinstance(name, str) else None, size)

   