
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.schemas import GradeCreate, GradeOut
from app.core import get_current_user
from app.services import grade_service

router = APIRouter(prefix="/grades", tags=["grades"])


@router.post("", response_model=GradeOut, status_code=status.HTTP_201_CREATED)
def record_grade(
    payload: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # headmaster OR teacher; ownership checked in service
):
    return grade_service.record_grade(db, payload, current_user)


@router.get("", response_model=List[GradeOut])
def list_grades(
    student_id: Optional[int] = None,
    subject: Optional[str] = None,
    term: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return grade_service.list_grades(db, current_user, student_id=student_id, subject=subject, term=term)