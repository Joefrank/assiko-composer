from typing import List, Optional
from Model.Score.Interval import Interval
from Model.Score.StaffLine import StaffLine


class NoteItemsList:   
    def __init__(self, line_notes: Optional[List[StaffLine]], interval_notes: Optional[List[Interval]]):
        self.line_notes: Optional[List[StaffLine]] = line_notes 
        self.interval_notes: Optional[List[Interval]] = interval_notes 
   