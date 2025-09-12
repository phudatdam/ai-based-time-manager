import datetime
from enum import Enum
from typing import List, Dict, Optional, Tuple

# FIle này chứa:
# class Task:
#     


# --- Enum và Type Hints ---

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Task:
    def __init__(self,
                 id: int,
                 description: str,
                 duration_minutes: int,
                 priority: Priority,
                 due_date: Optional[datetime.datetime] = None,
                 preferred_time: Optional[str] = None, # Ví dụ: "morning", "afternoon", "evening"
                 energy_level: Optional[str] = None, # Ví dụ: "high", "medium", "low"
                 project_id: Optional[str] = None,
                 scheduled_start: Optional[datetime.datetime] = None,
                 scheduled_end: Optional[datetime.datetime] = None): 
        self.id = id
        self.description = description
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.due_date = due_date
        self.preferred_time = preferred_time
        self.energy_level = energy_level
        self.project_id = project_id
        self.scheduled_start = scheduled_start
        self.scheduled_end = scheduled_end

    def __repr__(self) -> str:
        status = "Scheduled" if self.scheduled_start else "Pending"
        return (f"Task(id={self.id}, desc='{self.description}', prio={self.priority.name}, "
                f"duration={self.duration_minutes}min, status='{status}')")

class TimeSlot:
    def __init__(self, start: datetime.datetime, end: datetime.datetime):
        self.start = start
        self.end = end
        self.duration_minutes = int((end - start).total_seconds() / 60)

    def __repr__(self) -> str:
        return f"TimeSlot(start='{self.start.strftime('%H:%M')}', end='{self.end.strftime('%H:%M')}', duration={self.duration_minutes}min)"



