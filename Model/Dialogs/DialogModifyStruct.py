
class DialogModifyStruct:

    def __init__(self, main_window, dialog_title:str, dialog_message:str, target=None, buttons=[]):
        self.main_window = main_window
        self.dialog_title = dialog_title
        self.dialog_message = dialog_message
        self.target = target
        self.buttons = buttons