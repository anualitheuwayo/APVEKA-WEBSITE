from typing import Optional
from pydantic import BaseModel, ConfigDict


class SchoolClassCreate(BaseModel):
    """What the headmaster sends to create a new class."""
    name: str
    grade_level: Optional[str] = None


class SchoolClassUpdate(BaseModel):
    """All fields optional — you only send what you want to change."""
    name: Optional[str] = None
    grade_level: Optional[str] = None


class SchoolClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    grade_level: Optional[str]


class TeacherAssignmentCreate(BaseModel):
    """What the headmaster sends to assign a teacher to a class: POST /classes/{class_id}/teachers"""
    teacher_id: int


class ClassAssignmentOut(BaseModel):
    """One row from the class_assignments join table, returned after assigning a teacher."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    teacher_id: int
    class_id: int