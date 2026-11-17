from typing import Optional
from pydantic import BaseModel, ConfigDict


class TeacherOut(BaseModel):
    """A teacher's profile, as returned by GET /teachers — used to get a teacher's id
    so the headmaster can assign them to a class via ClassAssignment."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    full_name: str
    subject_specialty: Optional[str]
    phone: Optional[str]