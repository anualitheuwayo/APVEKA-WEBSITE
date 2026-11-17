from datetime import date
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AttendanceStatus


class AttendanceCreate(BaseModel):
    """What a teacher sends to mark attendance for one student, one day."""
    student_id: int
    class_id: int
    attendance_date: date = Field(default_factory=date.today)
    status: AttendanceStatus


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    class_id: int
    attendance_date: date
    status: AttendanceStatus