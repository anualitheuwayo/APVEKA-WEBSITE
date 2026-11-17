# app/repository/attendance_repository.py
"""Pure data-access for Attendance."""
from typing import Optional, List
from datetime import date as date_type
from sqlalchemy.orm import Session

from app.models import Attendance


def create(db: Session, *, recorded_by_id: int, **fields) -> Attendance:
    record = Attendance(**fields, recorded_by_id=recorded_by_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_filtered(db: Session, class_ids: Optional[List[int]] = None,
                   class_id: Optional[int] = None, student_id: Optional[int] = None,
                   attendance_date: Optional[date_type] = None) -> List[Attendance]:
    query = db.query(Attendance)
    if class_ids is not None:
        query = query.filter(Attendance.class_id.in_(class_ids))
    if class_id is not None:
        query = query.filter(Attendance.class_id == class_id)
    if student_id is not None:
        query = query.filter(Attendance.student_id == student_id)
    if attendance_date is not None:
        query = query.filter(Attendance.attendance_date == attendance_date)
    return query.all()