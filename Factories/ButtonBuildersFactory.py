
from Builders.ButtonBuilders import ButtonBuilder, ImageButtonBuilder, \
    SimpleButtonBuilder, StaggeredSymbolButtonBuilder, TimeSignatureButtonBuilder
from DataClasses.ButtonData import ButtonType


class ButtonBuildersFactory:

    @staticmethod 
    def get_button_builder(button_type) -> ButtonBuilder:
        if button_type == ButtonType.BUTTON:
            return SimpleButtonBuilder() 
        elif button_type == ButtonType.IMAGE_BUTTON:
            return ImageButtonBuilder()
        elif button_type == ButtonType.TIME_SIGNATURE_BUTTON:
            return TimeSignatureButtonBuilder()
        elif button_type == ButtonType.STAGGERED_SYMBOL_BUTTON:
            return StaggeredSymbolButtonBuilder()