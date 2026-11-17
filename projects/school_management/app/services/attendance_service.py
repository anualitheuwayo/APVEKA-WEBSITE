
from typing import Optional, List
from datetime import date as date_type
from fastapi import HTTPException

from app.models import User, RoleEnum, Attendance
from app.schemas import AttendanceCreate
from app.repository import attendance_repository as attendance_repo
from app.services import teacher_service


def _assert_can_touch_class(db, current_user: User, class_id: int) -> None:
    if current_user.role == RoleEnum.headmaster:
        return
    class_ids = teacher_service.class_ids_taught_by(db, current_user)
    if class_id not in class_ids:
        raise HTTPException(status_code=403, detail="You do not teach this class")


def record_attendance(db, payload: AttendanceCreate, current_user: User) -> Attendance:
    _assert_can_touch_class(db, current_user, payload.class_id)
    return attendance_repo.create(db, recorded_by_id=current_user.id, **payload.model_dump())


def list_attendance(db, current_user: User, class_id: Optional[int] = None,
                     student_id: Optional[int] = None,
                     attendance_date: Optional[date_type] = None) -> List[Attendance]:
    class_ids = None
    if current_user.role == RoleEnum.teacher:
        class_ids = teacher_service.class_ids_taught_by(db, current_user)
    return attendance_repo.list_filtered(
        db, class_ids=class_ids, class_id=class_id,
        student_id=student_id, attendance_date=attendance_date,
    )