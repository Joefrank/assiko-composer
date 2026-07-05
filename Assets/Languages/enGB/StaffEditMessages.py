

from dataclasses import dataclass


@dataclass
class StaffEditMessages:
    Confirm_Delete_Staff_Message = "Are you sure you want to delete this staff? click '{confirm}' to delete or '{cancel}' to keep it."
    Confirm_Delete_Staff_title = "Staff Deletion"