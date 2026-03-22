
from Model.Containers.Window import Window

class MainWindowRenderer:

    def __init__(self, main_window:Window):        
        self.main_window = main_window

    def render(self):
        self.main_window.draw()