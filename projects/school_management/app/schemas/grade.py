# app/schemas/grade.py
from pydantic import BaseModel, ConfigDict


class GradeCreate(BaseModel):
    """What a teacher sends to record one subject score for one student."""
    student_id: int
    subject: str
    term: str
    score: float
    max_score: float = 100.0


class GradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    subject: str
    term: str
    score: float
    max_score: float