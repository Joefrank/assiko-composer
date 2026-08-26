
class ButtonIcon:

    def __init__(self, symbol, tooltip_key, name, action=None, is_draggable=False, action_params=None):
        self.symbol = symbol
        self.tooltip = tooltip_key # this needs translation to be displayed in the tooltip.
        self.name = name
        self.action = action
        self.is_draggable = is_draggable
        self.action_params = action_params

