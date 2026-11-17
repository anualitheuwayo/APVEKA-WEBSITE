"""
Pure data-access for ClassAssignment — the join table that says
'this teacher teaches this class.' This is what makes Teacher <-> SchoolClass
many-to-many instead of one-to-one.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import ClassAssignment


def create(db: Session, *, teacher_id: int, class_id: int) -> ClassAssignment:
    assignment = ClassAssignment(teacher_id=teacher_id, class_id=class_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def exists(db: Session, teacher_id: int, class_id: int) -> bool:
    return db.query(ClassAssignment).filter(
        ClassAssignment.teacher_id == teacher_id,
        ClassAssignment.class_id == class_id,
    ).first() is not None


def class_ids_for_teacher(db: Session, teacher_id: int) -> List[int]:
    """All class ids a given teacher is assigned to teach."""
    rows = db.query(ClassAssignment.class_id).filter(
        ClassAssignment.teacher_id == teacher_id
    ).all()
    return [row[0] for row in rows]