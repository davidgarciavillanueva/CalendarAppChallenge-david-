from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar, List, Dict, Optional

from app.services.util import (
    generate_unique_id, date_lower_than_today_error, event_not_found_error,
    reminder_not_found_error, slot_not_available_error
)

@dataclass
class Reminder:
    date_time : datetime
    type: str = field(default="email")

    EMAIL: ClassVar[str] = "email"
    SYSTEM: ClassVar[str] = "system"

    def __str__(self) -> str:
        return f"Reminder on {self.date_time} of type {self.type}"

@dataclass
class Event:
    title: str
    description: str
    date_: date
    star_at: time
    end_at: time
    reminders: List[Reminder] = field(default_factory=list)
    id : str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL):
        reminder = Reminder(date_time,type_)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

    def __str__(self)-> str:
        return (f"ID: {self.id}\n"
                f"Event title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Time: {self.star_at} - {self.end_at}")

class Day:
    def __init__(self, date_: date):
        self.date_: date = date_
        self.slots: dict[time, str | None] = {}
        self._init_slots()
