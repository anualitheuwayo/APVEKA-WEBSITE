# app/services/grade_service.py
"""
Business rules for grades — this is where a teacher's marks are actually
captured and stored, with the same class-ownership rule as attendance.
"""
from typing import Optional, List
from fastapi import HTTPException

from app.models import User, RoleEnum, Grade
from app.schemas import GradeCreate
from app.repository import grade_repository as grade_repo
from app.repository import student_repository as student_repo
from app.services import teacher_service


def _assert_can_touch_student(db, current_user: User, student) -> None:
    if current_user.role == RoleEnum.headmaster:
        return
    class_ids = teacher_service.class_ids_taught_by(db, current_user)
    if student.class_id not in class_ids:
        raise HTTPException(status_code=403, detail="You do not teach this student's class")


def record_grade(db, payload: GradeCreate, current_user: User) -> Grade:
    student = student_repo.get_by_id(db, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    _assert_can_touch_student(db, current_user, student)
    return grade_repo.create(db, recorded_by_id=current_user.id, **payload.model_dump())


def list_grades(db, current_user: User, student_id: Optional[int] = None,
                 subject: Optional[str] = None, term: Optional[str] = None) -> List[Grade]:
    class_ids = None
    if current_user.role == RoleEnum.teacher:
        class_ids = teacher_service.class_ids_taught_by(db, current_user)
    return grade_repo.list_filtered(db, class_ids=class_ids, student_id=student_id, subject=subject, term=term)