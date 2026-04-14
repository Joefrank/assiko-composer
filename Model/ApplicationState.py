
class ApplicationState:
    """Manages the current state of the application.""" 

    def __init__(self):
        self.pending_dropped_item = None

    def save_dropped_symbol(self, rect, action, params_input):
        self.pending_dropped_item = (rect, action, params_input)

    def get_dropped_symbol(self):
        return self.pending_dropped_item
       