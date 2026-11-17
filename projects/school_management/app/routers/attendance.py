# app/routers/attendance.py
from typing import List, Optional
from datetime import date as date_type

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.schemas import AttendanceCreate, AttendanceOut
from app.core import get_current_user
from app.services import attendance_service

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def record_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # headmaster OR teacher; class-ownership checked in service
):
    return attendance_service.record_attendance(db, payload, current_user)


@router.get("", response_model=List[AttendanceOut])
def list_attendance(
    class_id: Optional[int] = None,
    student_id: Optional[int] = None,
    attendance_date: Optional[date_type] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return attendance_service.list_attendance(
        db, current_user, class_id=class_id, student_id=student_id, attendance_date=attendance_date
    )