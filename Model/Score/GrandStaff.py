

from __future__ import annotations

import copy

import pygame

from DataClasses.ControlData import ControlType
from Model.Dialogs.DialogModifyStruct import DialogModifyStruct
from Model.Score.ScoreControl import ScoreControl

class GrandStaff(ScoreControl):   
   
    def __init__(self, rect, name, staves=None, parent_page=None):
        super().__init__(rect=rect, control_type=ControlType.GRAND_STAFF, name=name, parent=parent_page)
        self.staves = [] if staves is None else list(staves)
        self.children = []
        for staff in self.staves:
            self.children.append(staff)
        self.set_positions()  # Set the top-left and bottom-right positions based on the staves

    def set_positions(self):
        if len(self.staves) > 0:
            self.top_left_position = self.staves[0].top_left_position
            self.bottom_right_position = self.staves[-1].bottom_right_position

    def add_staff(self, staff):
        self.staves.append(staff)
        self.children.append(staff)  # Add staff as a child control
        self.set_positions()  # Update positions after adding a new staff

    def delete(self):
        children = list(self.children)
        for child in children:
            if child is not None:
                child.delete()

        self.children.clear()
        self.staves.clear()

        if self.parent is not None:
            self.parent.unlink(self)
            self.parent = None

        if self.supported_events and self.get_app_state() is not None:
            self.get_app_state().get_window_event_handler().unsubscribe(self)

    def set_top_left_position(self, top_left):
        self.top_left_position = top_left

    def set_bottom_right_position(self, bottom_right):
        self.bottom_right_position = bottom_right

    def find_nearest_note(self, position):
        for staff in self.staves:
            note = staff.find_nearest_note(position)
            if note is not None:
                return note
        return None

    def get_top_left(self):
        if len(self.staves) > 0:
            return self.staves[0].top_left_position

    def get_bottom_left(self):
        no_of_staves = len(self.staves)
        if no_of_staves > 0:
            return self.staves[no_of_staves - 1].bottom_left_position

    def get_notes(self):
        notes = []
        for staff in self.staves:
            notes.extend(staff.get_notes())
        return notes
    
    def get_notes_offsets(self):
        if len(self.staves) > 0:
            return self.staves[0].get_notes_offsets()
        
    def get_chords(self):
        from Model.Score.Chord import Chord
        chords = []
        staff_count = 0
        for staff in self.staves:
            if staff_count == 0:
                chords.extend(staff.get_chords())
            else:
                staff_chords = staff.get_chords()
                for chord in staff_chords:
                    # find if chord with same x exists
                    existing_chord = next((c for c in chords if c.x_offset == chord.x_offset), None)
                    if existing_chord is not None:
                        # add notes to existing chord
                        existing_chord.append_chord(chord)
                    else:
                        chords.append(chord)
            staff_count += 1
        # sort all chords by x position
        chords.sort(key=lambda c: c.x_offset)
        return chords
    
    def get_initial_navigator_line(self):
        top_staff_top, _ = self.staves[0].get_initial_navigator_line()
        _, bottom_staff_bottom = self.staves[-1].get_initial_navigator_line() 
        top_left = copy.deepcopy(top_staff_top)
        bottom_left = copy.deepcopy(bottom_staff_bottom)
        return (top_left, bottom_left)
    
    def find_nearest_item_to_position(self, position):        
        for staff in self.staves:
            nearest_item = staff.find_nearest_item_to_position(position)
            if nearest_item is not None:
                return nearest_item
          
        return None
    
    """Move the grand staff and all its staves by the given offset in the y direction."""
    def move(self, _, offset_y):
        # Make sure grand staff doesn't exceed the boundaries of the parent page
        new_top = self.rect.top + offset_y
        new_bottom = self.rect.bottom + offset_y
        if new_top < 0 or new_bottom > self.parent.rect.height:
            return  # Do not move if it exceeds the boundaries
        for staff in self.staves:
            staff.move(0, offset_y) 
    
    def confirm_delete(self, caller):
        dialog_config = DialogModifyStruct(
            main_window=self.main_window,
            dialog_title=self.translate("CONFIRM_DELETE_GRANDSTAFF_TITLE"),
            dialog_message=self.translate("CONFIRM_DELETE_GRANDSTAFF_MESSAGE"),
            target=caller.parent            
        )
        callbacks = [self.delete_grand_staff, self.cancel_dialog]
        dialog = self.build_delete_confirm_dialog(caller, dialog_config, callbacks)
        dialog.show()

    def delete_grand_staff(self, target):
        target.delete()
        if target.last_opened_dialog:
             target.last_opened_dialog.close()
             target.last_opened_dialog = None  

    def draw(self, scrollable_screen):       
        previous_staff = None
        for staff in self.staves:
            # draw the staff
            staff.draw(scrollable_screen)
            # draw a line connecting the bottom of the previous staff to the top of the current staff
            if previous_staff is not None:
                # Adjust with scroll_y to ensure the line is drawn in the correct position relative to the viewport
                previous_staff_bottom_left = (previous_staff.bottom_left_position[0], previous_staff.bottom_left_position[1] - self.parent.scroll_y)
                staff_top_left = (staff.top_left_position[0], staff.top_left_position[1] - self.parent.scroll_y)
                pygame.draw.line(
                    scrollable_screen,
                    (0, 0, 0),
                    previous_staff_bottom_left,
                    staff_top_left,
                    2
                )
                # draw a vertical line connecting the right side of the previous staff to the right side of the current staff
                previous_staff_bottom_right = (previous_staff.bottom_right_position[0], previous_staff.bottom_right_position[1] - self.parent.scroll_y)
                staff_top_right = (staff.top_right_position[0], staff.top_right_position[1] - self.parent.scroll_y)
                pygame.draw.line(
                    scrollable_screen,
                    (0, 0, 0),
                    previous_staff_bottom_right,
                    staff_top_right,
                    2
                )
            previous_staff = staff
    