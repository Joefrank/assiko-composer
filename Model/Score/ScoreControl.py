
from typing import TYPE_CHECKING

from DataClasses.DialogConfigData import ConfirmDialogsConfig
from Model.Control import Control
from Model.Dialogs import DialogModifyStruct

if TYPE_CHECKING:
    from Model.Score.GrandStaff import GrandStaff
    from Model.Score.Staff import Staff

class ScoreControl(Control):

    def __init__(self, rect, control_type, name, parent):
        super().__init__(rect, control_type=control_type, name=name, parent=parent) 
        self.last_opened_dialog = None
        self.bg_color = (255,255,255)
        self.text_color = (40,40,40)

    def move(self, offset_x:int, offset_y:int):
        self.rect.x += offset_x
        self.rect.y += offset_y

    def move_y(self, offset_y:int):
        self.rect.y += offset_y

    def unlink(self, control):
        if control in self.children:
            self.children.remove(control)

            from Model.Score.GrandStaff import GrandStaff
            from Model.Score.Staff import Staff

            if isinstance(control, Staff) and isinstance(self, GrandStaff):
                self.staves.remove(control)
        
    """Score control can be deleted. All references should be set to null."""
    def delete(self):      
        self.parent.unlink(self)
        # Unsubscribe to events if any
        if self.supported_events and self.get_app_state() is not None:
            self.get_app_state().get_window_event_handler().unsubscribe(self)

        if not self.children or len(self.children) == 0:
            return
        
        for child in self.children:           
            child.delete()

    def map_coordinates_in_viewport(self, coordinates:tuple) -> tuple:
        return self.parent.map_coordinates_in_viewport(coordinates)
    
    def build_delete_confirm_dialog(self, caller, dialog_config:DialogModifyStruct, callbacks):
        common_dialog = self.main_window.common_dialog 
        caller.parent.last_opened_dialog = common_dialog 
        
        dialog_config.buttons = self.main_window.dialog_builder.create_dialog_buttons(
            ConfirmDialogsConfig.DIALOG_BUTTONS_CONFIG,
            common_dialog,
            callbacks=callbacks)       
        
        common_dialog.instantiate(dialog_config)        
        return common_dialog
    
    def cancel_dialog(self, target):
        if target.last_opened_dialog:
            target.last_opened_dialog.close()
            target.last_opened_dialog = None