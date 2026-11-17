# app/repository/grade_repository.py
"""Pure data-access for Grade — this is where a teacher's marks physically end up."""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Grade, Student


def create(db: Session, *, recorded_by_id: int, **fields) -> Grade:
    grade = Grade(**fields, recorded_by_id=recorded_by_id)
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


def list_filtered(db: Session, class_ids: Optional[List[int]] = None,
                   student_id: Optional[int] = None, subject: Optional[str] = None,
                   term: Optional[str] = None) -> List[Grade]:
    query = db.query(Grade)
    if class_ids is not None:
        # Grade has no class_id of its own — a mark belongs to a student, not a class directly.
        # So filtering "grades for classes I teach" means joining through Student to reach class_id.
        query = query.join(Student).filter(Student.class_id.in_(class_ids))
    if student_id is not None:
        query = query.filter(Grade.student_id == student_id)
    if subject is not None:
        query = query.filter(Grade.subject == subject)
    if term is not None:
        query = query.filter(Grade.term == term)
    return query.all()